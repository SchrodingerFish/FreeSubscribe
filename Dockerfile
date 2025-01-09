# 使用较小的 Python 基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 设置容器启动时运行的命令
CMD ["python", "main.py"]