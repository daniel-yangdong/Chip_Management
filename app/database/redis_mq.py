# redis_mq.py
import redis
import json
import logging
import time
from typing import Dict, Any, Callable, Optional
from threading import Thread


class RedisMessageQueue:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """初始化 Redis 消息队列连接"""
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )
        self.logger = logging.getLogger(__name__)
        self.consumers = {}

    def publish(self, channel: str, message: Dict[str, Any]) -> bool:
        """
        发布消息到指定频道

        Args:
            channel: 频道名称
            message: 消息内容

        Returns:
            bool: 发布是否成功
        """
        try:
            message_data = {
                'id': f"msg_{int(time.time() * 1000)}",
                'timestamp': time.time(),
                'data': message
            }
            self.redis_client.publish(channel, json.dumps(message_data))
            self.logger.info(f"Message published to channel {channel}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to publish message: {e}")
            return False

    def enqueue(self, queue_name: str, task: Dict[str, Any]) -> bool:
        """
        将任务加入队列（List 结构实现队列）

        Args:
            queue_name: 队列名称
            task: 任务数据

        Returns:
            bool: 入队是否成功
        """
        try:
            task_data = {
                'id': f"task_{int(time.time() * 1000)}",
                'created_at': time.time(),
                'data': task
            }
            self.redis_client.lpush(queue_name, json.dumps(task_data))
            self.logger.info(f"Task enqueued to {queue_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to enqueue task: {e}")
            return False

    def dequeue(self, queue_name: str, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """
        从队列中取出任务

        Args:
            queue_name: 队列名称
            timeout: 超时时间（秒），0表示阻塞等待

        Returns:
            Optional[Dict[str, Any]]: 任务数据
        """
        try:
            result = self.redis_client.brpop(queue_name, timeout=timeout)
            if result:
                _, task_json = result
                task_data = json.loads(task_json)
                self.logger.info(f"Task dequeued from {queue_name}")
                return task_data
            return None
        except Exception as e:
            self.logger.error(f"Failed to dequeue task: {e}")
            return None

    def subscribe(self, channels: list, callback: Callable[[str, Dict[str, Any]], None]):
        """
        订阅频道并处理消息

        Args:
            channels: 要订阅的频道列表
            callback: 消息处理回调函数
        """
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(*channels)

        def message_handler():
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        callback(message['channel'], data)
                    except Exception as e:
                        self.logger.error(f"Error handling message: {e}")

        # 启动监听线程
        thread = Thread(target=message_handler, daemon=True)
        thread.start()
        self.consumers[','.join(channels)] = {'thread': thread, 'pubsub': pubsub}

    def get_queue_length(self, queue_name: str) -> int:
        """获取队列长度"""
        return self.redis_client.llen(queue_name)

    def close(self):
        """关闭连接"""
        for consumer in self.consumers.values():
            if 'pubsub' in consumer:
                consumer['pubsub'].close()


# 全局消息队列实例
mq = RedisMessageQueue()
