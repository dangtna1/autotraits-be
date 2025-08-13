from sqlalchemy.orm import Session
from app.db.models.plant import Plant, PlantMeasurement, PlantFile
from app.schemas.plant import *

# ========= PLANT =========
def create_plant(db: Session, plant: PlantCreate):
    db_plant = Plant(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def get_plant(db: Session, plant_id: str):
    return db.query(Plant).filter(Plant.plant_id == plant_id).first()

def get_all_plants(db: Session):
    return db.query(Plant).all()

def delete_plant(db: Session, plant_id: str):
    plant = get_plant(db, plant_id)
    if plant:
        db.delete(plant)
        db.commit()
    return plant

# ========= MEASUREMENT =========
def create_measurement(db: Session, data: MeasurementCreate):
    db_obj = PlantMeasurement(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_measurement(db: Session, measurement_id: int):
    return db.query(PlantMeasurement).filter(PlantMeasurement.id == measurement_id).first()

def get_measurements(db: Session, plant_id: Optional[str] = None, date: Optional[date] = None):
    query = db.query(PlantMeasurement)
    if plant_id:
        query = query.filter(PlantMeasurement.plant_id == plant_id)
    if date:
        query = query.filter(PlantMeasurement.date == date)
    return query.all()

def update_measurement(db: Session, measurement_id: int, update_data: MeasurementUpdate):
    measurement = get_measurement(db, measurement_id)
    if measurement:
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(measurement, key, value)
        db.commit()
        db.refresh(measurement)
    return measurement

def delete_measurement(db: Session, measurement_id: int):
    measurement = get_measurement(db, measurement_id)
    if measurement:
        db.delete(measurement)
        db.commit()
    return measurement

# ========= FILE =========
def create_file(db: Session, data: FileCreate):
    db_file = PlantFile(**data.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: int):
    return db.query(PlantFile).filter(PlantFile.id == file_id).first()

def get_files(db: Session, plant_id: Optional[str] = None, file_type: Optional[str] = None):
    query = db.query(PlantFile)
    if plant_id:
        query = query.filter(PlantFile.plant_id == plant_id)
    if file_type:
        query = query.filter(PlantFile.file_type == file_type)
    return query.all()

def delete_file(db: Session, file_id: int):
    file = get_file(db, file_id)
    if file:
        db.delete(file)
        db.commit()
    return file