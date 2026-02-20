from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
from datetime import datetime
from jose import jwt

# ================= PRODUCTION CONFIG =================

URL = "postgresql://admin:arth_password@127.0.0.1:5433/gm_auth"
SECRET_KEY = "GRAPH_MIND_ULTIMATE_SECRET_KEY"
ALGORITHM = "HS256"

# ================= DATABASE =================

engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ================= MODEL =================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# ================= INIT =================

def init_db():
    Base.metadata.create_all(bind=engine)

# ================= SECURITY =================

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)