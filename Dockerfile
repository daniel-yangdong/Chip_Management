FROM python:3.9-slim

WORKDIR /app
ENV PYTHONPATH=/app
# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app/run.py"]
