from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .db import Base
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str):
        self.password_hash = ph.hash(password)

    def check_password(self, password: str):
        try:
            return ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False
