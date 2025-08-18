from sqlalchemy.orm import Session

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.models.plant import Plant

def ensure_plants_exist(db: Session, plant_ids: list[str]):
    existing_plants = (
        db.query(Plant.plant_id)
        .filter(Plant.plant_id.in_(plant_ids))
        .all()
    )
    existing_ids = {p[0] for p in existing_plants}
    
    missing_ids = set(plant_ids) - existing_ids

    if missing_ids:
        db.bulk_save_objects([Plant(plant_id=pid) for pid in missing_ids])
        db.commit()
        print(f"Inserted {len(missing_ids)} new plants: {missing_ids}")
    else:
        print("All plant_ids already exist.")
