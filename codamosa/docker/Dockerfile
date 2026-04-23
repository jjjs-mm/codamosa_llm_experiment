# 1. 构建阶段 (Build stage)
FROM python:3.10 AS build

# 设置环境变量，防止生成 pyc 文件和缓存输出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /pynguin-build

# 复制项目文件
COPY . .

# 安装依赖并构建
RUN pip install --upgrade pip \
    && pip install poetry==1.8.2 \
    && poetry config virtualenvs.create false \
    && poetry build

# 2. 运行阶段 (Execution stage)
FROM python:3.10 AS execute

# 设置运行所需环境变量
ENV PYNGUIN_DANGER_AWARE="1"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=0

WORKDIR /pynguin

# 从构建阶段拷贝编译好的包和脚本
COPY --from=build /pynguin-build/dist/pynguin-*.tar.gz .
# 修改为（从根目录尝试寻找）：
COPY --from=build /pynguin-build/pynguin-docker.sh .

# 安装并赋予脚本权限
RUN pip install /pynguin/pynguin-*.tar.gz \
    && chmod +x /pynguin/pynguin-docker.sh

ENTRYPOINT ["/pynguin/pynguin-docker.sh"]
CMD []