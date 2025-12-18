# Lang-LA 后端：Python 代理服务

本目录包含 Lang-LA 项目的 Python 后端，提供线性代数计算和可视化代理服务。

## 🎯 功能概述

- **计算代理** (`compute_agent.py`)：使用 NumPy 执行线性代数计算
- **可视化代理** (`visual_agent.py`)：生成 2D 线性变换的可视化图像
- **苏格拉底式教学代理** (`socratic_agent.py`)：通过提问引导学生学习，并记录学习点
- **学习分析代理** (`analysis_agent.py`)：基于历史数据提供个性化学习分析和建议
- **MySQL 数据库集成**：持久化存储学习点数据，支持历史分析和个性化建议
- **LangGraph 集成**：通过 `langgraph.json` 配置文件暴露代理接口
- **多模型支持**：兼容 OpenAI、DeepSeek 等 LLM 提供商

## 📋 系统要求

- Python 3.13+（推荐使用 uv 进行包管理）
- MySQL 5.7+ 或 MySQL 8.0+（用于存储学习点数据）
- 有效的 LLM API 密钥（OpenAI 或 DeepSeek）

## 🔧 安装与设置

### 1. 安装 uv（如果尚未安装）

```bash
# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 安装项目依赖

```bash
# 以下操作在本目录（src）执行

# 创建虚拟环境并安装依赖
uv venv
uv sync

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

### 3. 配置 MySQL 数据库

```bash
# 创建数据库（在 MySQL 中执行）
mysql -u root -p
CREATE DATABASE lang_la CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 4. 配置环境变量

```bash
# 复制环境变量示例文件
copy .env.example .env

# 编辑 .env 文件，填入以下内容：
# API_KEY=your_api_key_here
# API_BASE_URL=https://api.deepseek.com  # 或 https://api.openai.com/v1

# 数据库配置
# DB_HOST=localhost
# DB_PORT=3306
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=lang_la
```

### 5. 初始化数据库表

```bash
# 在虚拟环境中执行
python -m db.database
# 或直接运行
python db/database.py
```

这会自动创建 `learning_points` 表用于存储学习点数据。

## 🚀 运行代理服务

### 开发模式

```bash
# 确保在虚拟环境中
# 启动 LangGraph 开发服务器
langgraph serve

# 服务器将在 http://localhost:2024 启动
# 可用的图端点：
# - /compute-agent/playground
# - /visual-agent/playground
# - /socratic-agent/playground
# - /analysis-agent/playground
```

### 生产模式

```bash
# 使用生产配置启动
langgraph serve --host 0.0.0.0 --port 2024 --workers 4
```

## 🔌 API 端点

### 计算代理

- **端点**: `POST /compute-agent/invoke`
- **描述**: 执行线性代数计算
- **示例请求**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "计算矩阵 [[1,2],[3,4]] 的行列式"
    }
  ]
}
```

### 可视化代理

- **端点**: `POST /visual-agent/invoke`
- **描述**: 生成 2D 线性变换图像
- **示例请求**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "可视化矩阵 [[1,0.5],[0,1]] 的变换"
    }
  ]
}
```

### 苏格拉底式教学代理

- **端点**: `POST /socratic-agent/invoke`
- **描述**: 通过提问引导学生学习，并记录学习点
- **功能**:
  - 通过巧妙的提问引导学生自己发现答案
  - 记录学生的困惑点和薄弱环节到数据库
  - 支持图片识别和分析

### 学习分析代理

- **端点**: `POST /analysis-agent/invoke`
- **描述**: 基于历史数据提供个性化学习分析和建议
- **功能**:
  - 分析学生的学习统计信息（总记录数、难度分布、常见困惑点）
  - 获取最近的学习点记录
  - 根据知识点搜索相关历史记录
  - 深度分析学习模式和趋势
  - 提供个性化的学习建议

**示例请求**:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "分析我的学习情况，thread_id是xxx"
    }
  ]
}
```

### 健康检查

- **端点**: `GET /health`
- **描述**: 服务健康状态检查

## 📦 部署指南

### 选项一：Docker 部署（推荐）

#### 1. 创建 Dockerfile

在 `src` 目录下创建 `Dockerfile`：

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY .env.example .env
COPY . .

# 安装依赖
RUN uv sync --frozen

# 暴露端口
EXPOSE 2024

# 启动服务
CMD ["uv", "run", "langgraph", "serve", "--host", "0.0.0.0", "--port", "2024"]
```

#### 2. 构建并运行

```bash
# 构建镜像
docker build -t lang-la-backend .

# 运行容器
docker run -d \
  -p 2024:2024 \
  --name lang-la-backend \
  --env-file .env \
  lang-la-backend
```

## 🔐 环境变量

### LLM 配置

| 变量名 | 必填 | 默认值 | 描述 |
|--------|------|---------|------|
| `API_KEY` | 是 | - | LLM API 密钥 |
| `API_BASE_URL` | 是 | - | LLM API 基础 URL |

### 数据库配置

| 变量名 | 必填 | 默认值 | 描述 |
|--------|------|---------|------|
| `DB_HOST` | 否 | `localhost` | MySQL 主机地址 |
| `DB_PORT` | 否 | `3306` | MySQL 端口 |
| `DB_USER` | 否 | `root` | MySQL 用户名 |
| `DB_PASSWORD` | 是 | - | MySQL 密码 |
| `DB_NAME` | 否 | `lang_la` | MySQL 数据库名 |

### LangSmith 配置（可选）

| 变量名 | 必填 | 默认值 | 描述 |
|--------|------|---------|------|
| `LANGCHAIN_TRACING_V2` | 否 | `false` | 启用 LangSmith 追踪 |
| `LANGCHAIN_PROJECT` | 否 | `lang-la` | LangSmith 项目名称 |
| `LANGSMITH_API_KEY` | 否 | - | LangSmith API 密钥 |

## 🔧 故障排除

### 常见问题

1. **端口冲突**

    ``` bash
   错误：Address already in use
    ```

   **解决方案**：更改端口 `--port 2025` 或终止占用进程

2. **缺少依赖**

   ``` bash
   ModuleNotFoundError: No module named 'langchain'
   ```

   **解决方案**：运行 `uv sync` 重新安装依赖

3. **API 密钥无效**

   ``` bash
   AuthenticationError: Incorrect API key provided
   ```

   **解决方案**：检查 `.env` 文件中的 `API_KEY` 和 `API_BASE_URL`

4. **内存不足**
   **解决方案**：减少工作线程数 `--workers 2`

5. **数据库连接失败**

   ```bash
   pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")
   ```

   **解决方案**：
   - 确保 MySQL 服务正在运行
   - 检查 `.env` 文件中的数据库配置是否正确
   - 确认数据库用户有足够的权限
   - 运行 `python db/database.py` 初始化数据库表

6. **数据库表不存在**

   ```bash
   pymysql.err.ProgrammingError: (1146, "Table 'lang_la.learning_points' doesn't exist")
   ```

   **解决方案**：运行 `python db/database.py` 初始化数据库表

## 🔄 更新与维护

### 更新依赖

```bash
uv sync --upgrade
```

### 更新代码

```bash
git pull origin main # 该命令在根目录执行
uv sync
docker-compose restart  # 如果使用 Docker
```

---
**提示**：前端部署请参考项目根目录的 README.md 文件。
