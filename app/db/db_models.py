from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN, ForeignKey, FLOAT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    googleId = Column("google_id", String, unique=True)
    vkId = Column("vk_id", String, unique=True)
    appleId = Column("apple_id", String, unique=True)
    email = Column("email", String, unique=True)
    emailVerified = Column("email_verified", BOOLEAN, nullable=False)
    phone = Column("phone", Integer, unique=True)
    phoneVerified = Column("phone_verified", BOOLEAN, nullable=False)
    password = Column("password", String)
    name = Column("name", String)
    surname = Column("surname", String)
    username = Column("username", String, unique=True)
    rating = Column("rating", Integer)
    photoId = Column("photo_id", Integer, ForeignKey("photos.id"))
    roleId = Column("roleId", Integer, ForeignKey("roles.id"), nullable=False)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
    updatedAt = Column("updated_at", TIMESTAMP)
    lastLoginAt = Column("last_login_at", TIMESTAMP)
    deletedAt = Column("deleted_at", TIMESTAMP)
    emailVerifiedAt = Column("email_verified_at", TIMESTAMP)
    phoneVerifiedAt = Column("phone_verified_at", TIMESTAMP)

    photo = relationship("Photo", back_populates="owner")
    role = relationship("Role", back_populates="owner")
    vacancies = relationship("Vacancy", back_populates="user")


class Photo(Base):
    __tablename__ = "photos"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    url = Column("url", String)

    owner = relationship("User", back_populates="photo")


class Role(Base):
    __tablename__ = "roles"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column("title", String)

    owner = relationship("User", back_populates="role")


class Post(Base):
    __tablename__ = "posts"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    title = Column("title", String)
    description = Column("description", String)
    priceAmount = Column("price_amount", Integer)
    priceCurrency = Column("price_currency", String)
    link = Column("link", String)
    date = Column("date", TIMESTAMP)
    source = Column("source", String)
    parseDate = Column("parse_date", TIMESTAMP)
    priority = Column("priority", Integer)


class Jobs(Base):
    __tablename__ = "jobs"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    posts_parsed = Column("posts_parsed", Integer)
    posts_uploaded = Column("posts_uploaded", Integer)
    posts_update = Column("posts_update", Integer)
    posts_delete = Column("posts_delete", Integer)
    errors = Column("errors", Integer)
    lead_time = Column("lead_time", FLOAT)
    date = Column("date", TIMESTAMP)


class Errors(Base):
    __tablename__ = "errors"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    error = Column("error", String)
    description = Column("description", String)
    source = Column("source", String)
    job_id = Column("job_id", Integer)


class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    userId = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    title = Column("title", String(300), nullable=False)
    description = Column("description", String(6000))
    budget = Column("budget", Integer, default=None)
    name = Column("name", String)
    email = Column("email", String)
    phone = Column("phone", String)
    createdAt = Column("created_at", TIMESTAMP)

    links = relationship("File")
    user = relationship("User", back_populates="vacancies")


class File(Base):
    __tablename__ = "files"
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    filename = Column("filename", String)
    patch = Column("patch", String)
    vacancyId = Column("vacancy_id", Integer, ForeignKey("vacancies.id"))
