from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from app.models.base import Base, db


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True, autoincrement=True)
    music_name = Column(String(24), unique=True, nullable=False)
    author = Column(String(24), nullable=False)
    file_path = Column(String(100), nullable=False)
    categoryId = Column(Integer, ForeignKey('category.id'), nullable=True)


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False)
