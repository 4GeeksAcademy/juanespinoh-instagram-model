from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
from sqlalchemy import String, Boolean,ForeignKey,Table,Column
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name:Mapped[str] =mapped_column(String(100), nullable=False)
    bio:Mapped[str] =mapped_column(String(300), nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    created: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name":self.user_name,
            "bio":self.bio,
            "is_active":self.is_active,
            "created":self.created
            # do not serialize the password, its a security breach
        }
    
association_table = Table(
    "post_tag", db.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "posts"

    id:Mapped[int]=mapped_column(primary_key=True)
    image_url:Mapped[str] =mapped_column(nullable=False)
    caption:Mapped[str] =mapped_column(String(150),nullable=True)
    created: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="original_post", cascade="all, delete-orphan")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=association_table,
        back_populates="posts"
    )



    def serialize(self):
        return {
                "id": self.id,
                "image_url": self.image_url,
                "caption":self.caption,
                "user_id":self.user_id,
                "is_active":self.is_active,
                "created":self.created,
                "author":self.author.serialize()
            # do not serialize the password, its a security breach
        }

class Comment(db.Model):
    __tablename__="comments"

    id:Mapped[int]=mapped_column(primary_key=True)
    text:Mapped[str] =mapped_column(String(270), nullable=False)
    created: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    original_post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
                "id": self.id,
                "text": self.text,
                "caption":self.caption,
                "post_id":self.post_id,
                "original_post":self.original_post,
                "created":self.created,
            
        }
    

class Tag(db.Model):
    __tablename__="tags"

    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str] =mapped_column(String(50), nullable=False)
    post: Mapped[list["Post"]] = relationship(
        "Post",
        secondary=association_table,
        back_populates="tags"
    )




    
    def serialize(self):
        return {
                "id": self.id,
                "name": self.name
            
        }










