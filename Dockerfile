# 使用官方Python运行时作为父镜像
FROM python:3.8-slim

# 将工作目录设置为/app
WORKDIR /app

# 将当前目录内容复制到位于/app中的容器中
ADD . /app

# 安装requirements.txt中指定的任何所需包
RUN pip install --no-cache-dir flask pymongo

# 让端口5000可用于访问
EXPOSE 5000

# 定义环境变量
ENV NAME World

# 运行app.py当容器启动时
CMD ["python", "app.py"]
