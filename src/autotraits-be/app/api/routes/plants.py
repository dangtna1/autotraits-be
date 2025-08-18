from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.plant import *
from app.crud import plant as crud
from app.dependencies import get_db

router = APIRouter()

# ========== PLANTS ==========
@router.post("/plants/", response_model=PlantInDB)
def create_plant_route(plant: PlantCreate, db: Session = Depends(get_db)):
    return crud.create_plant(db, plant)

@router.get("/plants/", response_model=List[PlantInDB])
def list_plants_route(db: Session = Depends(get_db)):
    return crud.get_all_plants(db)

@router.get("/plants/{plant_id}", response_model=PlantInDB)
def get_plant_route(plant_id: str, db: Session = Depends(get_db)):
    plant = crud.get_plant(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@router.delete("/plants/{plant_id}", response_model=PlantInDB)
def delete_plant_route(plant_id: str, db: Session = Depends(get_db)):
    return crud.delete_plant(db, plant_id)

# ========== MEASUREMENTS ==========
@router.post("/measurements/", response_model=MeasurementInDB)
def create_measurement_route(measurement: MeasurementCreate, db: Session = Depends(get_db)):
    return crud.create_measurement(db, measurement)

@router.get("/measurements/", response_model=List[MeasurementInDB])
def list_measurements_route(plant_id: Optional[str] = None, date: Optional[date] = None, db: Session = Depends(get_db)):
    return crud.get_measurements(db, plant_id, date)

@router.get("/measurements/{measurement_id}", response_model=MeasurementInDB)
def get_measurement_route(measurement_id: int, db: Session = Depends(get_db)):
    measurement = crud.get_measurement(db, measurement_id)
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

@router.put("/measurements/{measurement_id}", response_model=MeasurementInDB)
def update_measurement_route(measurement_id: int, data: MeasurementUpdate, db: Session = Depends(get_db)):
    return crud.update_measurement(db, measurement_id, data)

@router.delete("/measurements/{measurement_id}", response_model=MeasurementInDB)
def delete_measurement_route(measurement_id: int, db: Session = Depends(get_db)):
    return crud.delete_measurement(db, measurement_id)

# ========== FILES ==========
@router.post("/files/", response_model=FileInDB)
def create_file_route(file: FileCreate, db: Session = Depends(get_db)):
    return crud.create_file(db, file)

@router.get("/files/", response_model=List[FileInDB])
def list_files_route(plant_id: Optional[str] = None, file_type: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_files(db, plant_id, file_type)

@router.get("/files/{file_id}", response_model=FileInDB)
def get_file_route(file_id: int, db: Session = Depends(get_db)):
    file = crud.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.delete("/files/{file_id}", response_model=FileInDB)
def delete_file_route(file_id: int, db: Session = Depends(get_db)):
    return crud.delete_file(db, file_id)