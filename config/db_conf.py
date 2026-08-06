import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

#数据库URL
load_dotenv()

ASYNC_DATABASE_URL = os.getenv("DATABASE_URL")

if not ASYNC_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured. Copy .env.example to .env and set it first.")

#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  #输出SQL日志
    pool_size=10,  #连接池大小
    max_overflow=20,  #连接池允许超出的连接数
)

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,      # 绑定引擎
    class_=AsyncSession,    # 指定会话类
    expire_on_commit=False, # 设置为False，表示会话对象在提交后不会自动关闭
)

#依赖项,用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
