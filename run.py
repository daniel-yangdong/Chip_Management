# run.py
from app import create_app

# 创建Flask应用实例
app = create_app()

if __name__ == '__main__':
    # 启动开发服务器
    app.run(
        debug=True,      # 启用调试模式
        host='0.0.0.0', # 监听所有网络接口
        port=5000       # 使用5000端口
    )