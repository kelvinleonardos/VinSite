from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from .config import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    about_me = Column(Text, nullable=True)
    role_ref_id = Column(Integer, ForeignKey('role_ref.id'), nullable=False)

    blogs = relationship('Blog', back_populates='user')
    achievements = relationship('Achievement', back_populates='user')
    portfolios = relationship('Portfolio', back_populates='user')
    experiences = relationship('Experience', back_populates='user')
    social_medias = relationship('SocialMedia', back_populates='user')
    comments = relationship('Comment', back_populates='user')


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_draft = Column(Boolean, default=False, nullable=False)
    category_ref_id = Column(Integer, ForeignKey('category_ref.id'), nullable=True)

    user = relationship('User', back_populates='blogs')


class Achievement(Base):
    __tablename__ = 'achievement'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_draft = Column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='achievements')


class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    portfolio_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_draft = Column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='portfolios')


class Experience(Base):
    __tablename__ = 'experience'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_draft = Column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='experiences')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    post_ref_id = Column(Integer, ForeignKey('post_ref.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text, nullable=False)

    user = relationship('User', back_populates='comments')


class SocialMedia(Base):
    __tablename__ = 'social_media'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    icon_url = Column(String(255), nullable=False)
    profile_url = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='social_medias')


class PostRef(Base):
    __tablename__ = 'post_ref'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)


class RoleRef(Base):
    __tablename__ = 'role_ref'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)


class CategoryRef(Base):
    __tablename__ = 'category_ref'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
