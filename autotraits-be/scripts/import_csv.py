import argparse
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.db.session import SessionLocal
from app.db.models.plant import PlantMeasurement
from scripts.import_utils import ensure_plants_exist
import math

def clean_nan_dict(d):
    return {
        k: None if (isinstance(v, float) and math.isnan(v)) else v
        for k, v in d.items()
    }


def parse_date(d):
    return datetime.strptime(str(d), "%Y%m%d").date()

def import_2d_traits(filepath: str):
    df = pd.read_csv(filepath, delimiter=',')  # or use comma if CSV is comma-separated
    
    df.rename(columns={
        "ID": "plant_id",
        "Date": "date",
        "Ripe": "ripe",
        "Part-ripe": "part_ripe",
        "Unripe": "unripe",
        "Flower": "flower",
        "Fruit-width": "fruit_width",
        "Fruit-height": "fruit_height",
        "Mass": "mass",
        "Yield/plant": "yield_per_plant",
        "Crop-composition": "crop_composition",
        "Plant-height": "plant_height",
        "ExG": "exg",
    }, inplace=True)

    df["date"] = df["date"].apply(lambda x: parse_date(x) if pd.notnull(x) else None)
    df = df.where(pd.notnull(df), None)

    session: Session = SessionLocal()
    # Ensure plants exist first
    plant_ids = df["plant_id"].unique().tolist()
    ensure_plants_exist(session, plant_ids)
    
    try:
        for _, row in df.iterrows():
            row = clean_nan_dict(row.to_dict())

            existing = session.query(PlantMeasurement).filter_by(
                plant_id=row["plant_id"],
                date=row["date"]
            ).first()

            if existing:
                # Update only biomass and canopy_density
                existing.ripe = row["ripe"]
                existing.part_ripe = row["part_ripe"]
                existing.unripe = row["unripe"]
                existing.flower = row["flower"]
                existing.fruit_width = row["fruit_width"]
                existing.fruit_height = row["fruit_height"]
                existing.mass = row["mass"]
                existing.yield_per_plant = row["yield_per_plant"]
                existing.crop_composition = row["crop_composition"]
                existing.plant_height = row["plant_height"]
                existing.exg = row["exg"]
            else:
                entry = PlantMeasurement(**row)
                session.add(entry)
                
        session.commit()
        print(f"Imported {len(df)} measurement records from {filepath}")
    except Exception as e:
        session.rollback()
        print(f"Error importing measurements: {e}")
    finally:
        session.close()

def import_3D_traits(filepath: str):
    df = pd.read_csv(filepath, delimiter=',')

    df.rename(columns={
        "ID": "plant_id",
        "Date": "date",
        "Biomass": "biomass",
        "CanopyDensity": "canopy_density"
    }, inplace=True)

    df["date"] = df["date"].apply(parse_date)
    df = df.where(pd.notnull(df), None)

    session: Session = SessionLocal()

    # Ensure plants exist first
    plant_ids = df["plant_id"].unique().tolist()
    ensure_plants_exist(session, plant_ids)

    try:
        for _, row in df.iterrows():
            row = clean_nan_dict(row.to_dict())

            existing = session.query(PlantMeasurement).filter_by(
                plant_id=row["plant_id"],
                date=row["date"]
            ).first()

            if existing:
                # Update only biomass and canopy_density
                existing.biomass = row["biomass"]
                existing.canopy_density = row["canopy_density"]
            
            else:
                # Insert new record
                new_entry = PlantMeasurement(**row)
                session.add(new_entry)
           
        session.commit()
        print(f"Imported or updated {len(df)} biomass records from {filepath}")
    except Exception as e:
        session.rollback()
        print(f"Error importing biomass: {e}")
    finally:
        session.close()

def main():
    parser = argparse.ArgumentParser(description="Import 2D traits or 3D traits from a CSV file")
    parser.add_argument("--type", choices=['2D', '3D'], required=True, help="2D or 3D traits")
    parser.add_argument("--file", required=True, type=str, help="Path to the CSV file")
    
    args = parser.parse_args()

    if args.type == "2D":
        import_2d_traits(args.file)
    elif args.type == "3D":
        import_3D_traits(args.file)
    else:
        print("Invalid type specified. Use '2D' or '3D'.")

if __name__ == "__main__":
    main()