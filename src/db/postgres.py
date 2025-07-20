from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.core import config

Base = declarative_base()

engine = create_async_engine(
    config.DATABASE_DSN, 
    echo=True, 
    future=True,
    pool_pre_ping=True,
    pool_recycle=300
)

async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_database() -> None:
    """Create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)


async def purge_database() -> None:
    """Drop all tables from the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)