# Database Optimization
# construction-platform/python-services/api/db_optimization.py

from sqlalchemy import create_engine, pool, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
import logging
from typing import Generator
import os

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """Database optimizer with connection pooling and query optimization"""
    def __init__(self, database_url: str, pool_size: int = 20, max_overflow: int = 10):
        self.database_url = database_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        
        # Create engine with connection pooling and ACID compliance
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,  # Verify connections before using
            pool_recycle=3600,   # Recycle connections after 1 hour
            echo=False,
            # ACID compliance settings
            isolation_level="READ COMMITTED",  # Default PostgreSQL isolation
            connect_args={
                "options": "-c default_transaction_isolation=read committed"
            }
        )
        
        # Create session factory
        self.SessionLocal = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
        )
        
        logger.info(f"Database optimizer initialized: pool_size={pool_size}, max_overflow={max_overflow}")
    
    @contextmanager
    def get_session(self) -> Generator:
        """Get database session with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    @contextmanager
    def get_transaction(self, isolation_level: str = "READ COMMITTED") -> Generator:
        """Get database session with ACID-compliant transaction"""
        session = self.SessionLocal()
        try:
            # Set isolation level for ACID compliance
            session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
            logger.info(f"Transaction started with isolation level: {isolation_level}")
            yield session
            session.commit()
            logger.info("Transaction committed successfully")
        except Exception as e:
            session.rollback()
            logger.error(f"Transaction rolled back due to error: {e}", exc_info=True)
            raise
        finally:
            session.close()

    
    def optimize_queries(self, query):
        """Optimize database queries"""
        # Add query optimization logic here
        # - Use indexes
        # - Limit result sets
        # - Use eager loading for relationships
        # - Avoid N+1 queries
        return query
    
    def get_connection_stats(self) -> dict:
        """Get connection pool statistics"""
        pool = self.engine.pool
        return {
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.invalid()
        }

# Global database optimizer instance
db_optimizer = None

def initialize_db_optimizer(database_url: str = None, pool_size: int = 20, max_overflow: int = 10):
    """Initialize database optimizer"""
    global db_optimizer
    if database_url is None:
        database_url = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/construction_ai"
        )
    db_optimizer = DatabaseOptimizer(database_url, pool_size, max_overflow)
    return db_optimizer
