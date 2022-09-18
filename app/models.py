from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, String
from .database import Base
from sqlalchemy.sql.expression import null, text


class Post(Base):

    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
