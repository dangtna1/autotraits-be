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
from sqlalchemy.orm import relationship
from app.db.base import Base


class Plant(Base):
    __tablename__ = "plants"
    breeder_id = Column(Integer, ForeignKey("breeders.id"), nullable=False)
    plant_id = Column(String, primary_key=True)

    breeder = relationship("Breeder", back_populates="plants")
    measurements = relationship(
        "PlantMeasurement", back_populates="plant", cascade="all, delete"
    )
    files = relationship("PlantFile", back_populates="plant", cascade="all, delete")


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
    plant = relationship("Plant", back_populates="measurements")
    __table_args__ = (UniqueConstraint("plant_id", "date", name="uix_plant_date"),)


class PlantFile(Base):
    __tablename__ = "plant_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(String, ForeignKey("plants.plant_id"))
    date = Column(Date)
    file_path = Column(String)
    file_type = Column(String)
    plant = relationship("Plant", back_populates="files")
