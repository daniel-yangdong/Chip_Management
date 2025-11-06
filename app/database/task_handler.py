# task_handler.py
import threading
import time
import logging
from typing import Dict, Any, Callable
from redis_mq import mq


class TaskWorker:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.task_handlers = {}
        self.workers = []
        self.running = False

    def register_handler(self, task_type: str, handler: Callable[[Dict[str, Any]], None]):
        """
        注册任务处理器

        Args:
            task_type: 任务类型
            handler: 处理函数
        """
        self.task_handlers[task_type] = handler
        self.logger.info(f"Registered handler for task type: {task_type}")

    def process_task(self, task_data: Dict[str, Any]):
        """
        处理单个任务

        Args:
            task_data: 任务数据
        """
        try:
            task_type = task_data.get('data', {}).get('type')
            if task_type in self.task_handlers:
                self.logger.info(f"Processing task: {task_type}")
                self.task_handlers[task_type](task_data['data'])
                self.logger.info(f"Task processed successfully: {task_type}")
            else:
                self.logger.warning(f"No handler found for task type: {task_type}")
        except Exception as e:
            self.logger.error(f"Error processing task: {e}")
            # 可以将失败的任务发送到死信队列
            self.handle_failed_task(task_data, str(e))

    def handle_failed_task(self, task_data: Dict[str, Any], error: str):
        """
        处理失败的任务

        Args:
            task_data: 任务数据
            error: 错误信息
        """
        failed_task = {
            **task_data,
            'error': error,
            'failed_at': time.time()
        }
        mq.enqueue('failed_tasks', failed_task)

    def start_worker(self, queue_name: str, worker_count: int = 1):
        """
        启动工作进程

        Args:
            queue_name: 队列名称
            worker_count: 工作进程数量
        """
        self.running = True

        def worker_process():
            self.logger.info(f"Worker started for queue: {queue_name}")
            while self.running:
                try:
                    task_data = mq.dequeue(queue_name, timeout=5)
                    if task_data:
                        self.process_task(task_data)
                except Exception as e:
                    self.logger.error(f"Error in worker process: {e}")
                    time.sleep(1)
            self.logger.info(f"Worker stopped for queue: {queue_name}")

        # 启动多个工作进程
        for i in range(worker_count):
            worker_thread = threading.Thread(target=worker_process, daemon=True)
            worker_thread.start()
            self.workers.append(worker_thread)
            self.logger.info(f"Started worker {i + 1} for queue: {queue_name}")

    def stop_workers(self):
        """停止所有工作进程"""
        self.running = False
        for worker in self.workers:
            worker.join(timeout=5)
        self.logger.info("All workers stopped")


# 全局任务处理器实例
task_worker = TaskWorker()
