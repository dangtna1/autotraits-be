from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models so their tables are registered in Base.metadata
from app.db.models import user
from app.db.models import breeder
from app.db.models import plant
