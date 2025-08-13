from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# ======== PLANT ========
class PlantBase(BaseModel):
    plant_id: str

class PlantCreate(PlantBase):
    pass

class PlantInDB(PlantBase):
    class Config:
        form_attributes = True

# ======== MEASUREMENT ========
class MeasurementBase(BaseModel):
    plant_id: str
    date: date
    biomass: Optional[float] = None
    canopy_density: Optional[float] = None
    ripe: Optional[int] = None
    part_ripe: Optional[int] = None
    unripe: Optional[int] = None
    flower: Optional[int] = None
    fruit_width: Optional[float] = None
    fruit_height: Optional[float] = None
    mass: Optional[float] = None
    yield_per_plant: Optional[float] = None
    crop_composition: Optional[float] = None
    plant_height: Optional[float] = None
    exg: Optional[float] = None

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementUpdate(BaseModel):
    biomass: Optional[float]
    canopy_density: Optional[float]
    # other fields optional
    ripe: Optional[int] = None
    # ...

class MeasurementInDB(MeasurementBase):
    id: int

    class Config:
        form_attributes = True

# ======== FILE ========
class FileBase(BaseModel):
    plant_id: str
    date: date
    file_path: str
    file_type: str

class FileCreate(FileBase):
    pass

class FileInDB(FileBase):
    id: int

    class Config:
        form_attributes = True
