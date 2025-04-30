from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.engine import URL

import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    database=os.getenv("DATABASE_NAME")
)



engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        # Uncomment the following line to drop all tables (be careful in production)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()