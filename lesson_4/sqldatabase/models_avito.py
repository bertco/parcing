from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# associative_img_post = Table('associative_tag_post', Base.metadata,
#                              Column('blog_post', Integer, ForeignKey('Apt_post.id')),
#                              Column('blog_images', Integer, ForeignKey('images.id'))
#                              )

class AptPost(Base):
    __tablename__ = 'Apt_post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    title = Column(String)
    price = Column(String)
    # images = relationship('Images', secondary=associative_img_post, backref='posts')
    author_url = Column(String)
    address = Column(String)
    # author = Column(Integer, ForeignKey('authors.id'))
    # authors = relationship('Authors', backref='posts')
    # tags = relationship('Tags', secondary=associative_tag_post, backref='posts')


    def __init__(self, title, url, price, author_url, address):
        self.title = title
        self.url = url
        self.price = price
        # if image:
        # self.images.extend(images)
        self.author_url = author_url
        self.address = address

# class Tags(Base):
#     __tablename__ = 'tags'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String)
#     url = Column(String, unique=True)
#
#     def __init__(self, title, url):
#         self.title = title
#         self.url = url

class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_url = Column(String, unique=True)
    #name = Column(String)

    def __init__(self, author_url):
        self.author_url = author_url
        # self.name = name

class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String, unique=True)

    def __init__(self, image_url):
        self.image_url = image_url