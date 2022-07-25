from sqlalchemy import Column, BigInteger, String, TIMESTAMP, BOOLEAN, ForeignKey, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    googleId = Column("google_id", String, unique=True)
    vkId = Column("vk_id", String, unique=True)
    appleId = Column("apple_id", String, unique=True)
    email = Column("email", String, unique=True)
    emailVerified = Column("email_verified", BOOLEAN, nullable=False)
    phone = Column("phone", BigInteger, unique=True)
    phoneVerified = Column("phone_verified", BOOLEAN, nullable=False)
    password = Column("password", String)
    name = Column("name", String)
    surname = Column("surname", String)
    username = Column("username", String, unique=True)
    rating = Column("rating", BigInteger)
    photoId = Column("photo_id", BigInteger, ForeignKey("photos.id"))
    roleId = Column("roleId", BigInteger, ForeignKey("roles.id"), nullable=False)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
    updatedAt = Column("updated_at", TIMESTAMP)
    lastLoginAt = Column("last_login_at", TIMESTAMP)
    deletedAt = Column("deleted_at", TIMESTAMP)
    emailVerifiedAt = Column("email_verified_at", TIMESTAMP)
    phoneVerifiedAt = Column("phone_verified_at", TIMESTAMP)

    photo = relationship("Photo", back_populates="owner")
    role = relationship("Role", back_populates="owner")
    vacancies = relationship("Vacancy", back_populates="user")
    shoutouts = relationship("Shoutout", back_populates="user")
    posts = relationship("Favorites")
    historySearch = relationship("HistorySearch")


class Photo(Base):
    __tablename__ = "photos"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    url = Column("url", String)

    owner = relationship("User", back_populates="photo")


class Role(Base):
    __tablename__ = "roles"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column("title", String)

    owner = relationship("User", back_populates="role")


class Post(Base):
    __tablename__ = "posts"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    random = Column("random", BigInteger)
    title = Column("title", String)
    description = Column("description", String)
    priceAmount = Column("price_amount", BigInteger)
    priceCurrency = Column("price_currency", String)
    link = Column("link", String)
    date = Column("date", TIMESTAMP)
    source = Column("source", String)
    parseDate = Column("parse_date", TIMESTAMP)
    priority = Column("priority", BigInteger)


class Jobs(Base):
    __tablename__ = "jobs"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    posts_parsed = Column("posts_parsed", BigInteger)
    posts_uploaded = Column("posts_uploaded", BigInteger)
    posts_update = Column("posts_update", BigInteger)
    posts_delete = Column("posts_delete", BigInteger)
    errors = Column("errors", BigInteger)
    lead_time = Column("lead_time", FLOAT)
    date = Column("date", TIMESTAMP)


class Errors(Base):
    __tablename__ = "errors"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    error = Column("error", String)
    description = Column("description", String)
    source = Column("source", String)
    job_id = Column("job_id", BigInteger)


class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    userId = Column("user_id", BigInteger, ForeignKey("users.id"), nullable=False)
    title = Column("title", String(300), nullable=False)
    description = Column("description", String(6000))
    budget = Column("budget", BigInteger, default=None)
    name = Column("name", String)
    email = Column("email", String)
    phone = Column("phone", String)
    createdAt = Column("created_at", TIMESTAMP)

    user = relationship("User", back_populates="vacancies")


class File(Base):
    __tablename__ = "files"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    filename = Column("filename", String)
    patch = Column("patch", String)
    vacancyId = Column("vacancy_id", BigInteger, ForeignKey("vacancies.id"))


class Favorites(Base):
    __tablename__ = "favorites"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    userId = Column("user_id", BigInteger, ForeignKey("users.id"))
    objId = Column("obj_id", BigInteger, ForeignKey("posts.id"))


class Shoutout(Base):
    __tablename__ = "shoutout"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    userId = Column("user_id", BigInteger, ForeignKey("users.id"))
    text = Column("text", String, nullable=False)
    rating = Column("rating", BigInteger, nullable=False)
    createdAt = Column("created_at", TIMESTAMP)

    user = relationship("User", back_populates="shoutouts")


class HistorySearch(Base):
    __tablename__ = "history_search"
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    userId = Column("user_id", BigInteger, ForeignKey("users.id"))
    searchQuery = Column("search_query", String)
    withContractPrice = Column("with_contract_price", BOOLEAN)
    price = Column("price", BigInteger)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
