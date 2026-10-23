
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

print("CloudGuard database tables created successfully.")
