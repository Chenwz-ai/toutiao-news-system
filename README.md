# 新闻资讯系统

一个前后端分离的新闻资讯项目。目前已完成新闻模块，包括新闻分类、列表、详情、浏览量统计和相关推荐。

## 技术栈

- 后端：Python、FastAPI、SQLAlchemy、MySQL、aiomysql
- 前端：Vue 3、Vite、Pinia、Vue Router、Vant、Axios

## 项目结构

```text
.
├── main.py                         # FastAPI 入口
├── routers/                        # 新闻接口路由
├── crud/                           # 数据库查询逻辑
├── models/                         # SQLAlchemy 数据模型
├── config/                         # 后端配置
├── 数据库sql文件/database.sql       # 数据库表结构和演示新闻数据
└── 前端项目代码/xwzx-news/          # Vue 前端项目
```

## 本地运行

### 1. 准备数据库

在 MySQL 中执行 [数据库sql文件/database.sql](数据库sql文件/database.sql)，创建 `news_app` 数据库、表和演示数据。

### 2. 启动后端

要求：Python 3.10+、MySQL 8+。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

编辑 `.env`，将 `DATABASE_URL` 中的 `your-password` 改成你的 MySQL 密码；随后启动服务：

```powershell
uvicorn main:app --reload
```

后端默认运行在 `http://127.0.0.1:8000`，接口文档为 `http://127.0.0.1:8000/docs`。

### 3. 启动前端

要求：Node.js 18+。

```powershell
Set-Location "前端项目代码/xwzx-news"
npm install
Copy-Item .env.example .env.local
npm run dev
```

前端默认请求 `http://127.0.0.1:8000`。如需启用 AI 问答，可在 `.env.local` 配置 `VITE_DASHSCOPE_API_KEY`。

> 注意：`VITE_*` 变量会被打包到浏览器中，不能用来保存正式环境的私密 API Key。生产环境应让后端代为调用 AI 服务。

## 已实现接口

| 功能 | 接口 |
| --- | --- |
| 获取新闻分类 | `GET /api/news/categories` |
| 获取新闻列表 | `GET /api/news/list?categoryId=1&page=1&pageSize=10` |
| 获取新闻详情 | `GET /api/news/detail?id=1` |

更完整的接口说明见 [API接口规范文档.md](API接口规范文档.md)。

## 安全说明

- `.env`、前端 `.env.local`、虚拟环境、依赖目录和 IDE 配置已通过 `.gitignore` 排除。
- 不要提交数据库密码、API Key、访问令牌或真实用户数据。
- 如凭据曾被提交到公开仓库，必须在服务商后台撤销并重新生成，而不只是从代码中删除。
