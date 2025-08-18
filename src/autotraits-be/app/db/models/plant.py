from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Breeder(Base):
    __tablename__ = "breeders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="breeder")
    plants = relationship("Plant", back_populates="breeder")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    role = Column(String, default="user")  # user/admin
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=False)

    breeder = relationship("Breeder", back_populates="users")


class Plant(Base):
    __tablename__ = "plants"
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=False)
    plant_id = Column(String, primary_key=True)

    breeder = relationship("Breeder", back_populates="plants")


class PlantMeasurement(Base):
    __tablename__ = "plant_measurements"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(String, ForeignKey("plants.plant_id"))
    date = Column(Date)
    biomass = Column(Float, nullable=True)
    canopy_density = Column(Float, nullable=True)
    ripe = Column(Integer, nullable=True)
    part_ripe = Column(Integer, nullable=True)
    unripe = Column(Integer, nullable=True)
    flower = Column(Integer, nullable=True)
    fruit_width = Column(Float, nullable=True)
    fruit_height = Column(Float, nullable=True)
    mass = Column(Float, nullable=True)
    yield_per_plant = Column(Float, nullable=True)
    crop_composition = Column(Float, nullable=True)
    plant_height = Column(Float, nullable=True)
    exg = Column(Float, nullable=True)
    __table_args__ = (UniqueConstraint("plant_id", "date", name="uix_plant_date"),)


class PlantFile(Base):
    __tablename__ = "plant_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(String, ForeignKey("plants.plant_id"))
    date = Column(Date)
    file_path = Column(String)
    file_type = Column(String)
