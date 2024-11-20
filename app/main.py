from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from app.dependencies import get_current_user
from app.routers import appointment_routers, auth_routers, patient_routers, provider_routers
from app.db.session import init_db, SessionLocal
import pandas as pd
from app.models import provider_models

# Create FastAPI instance
app = FastAPI(
    title="Health Info System API",
)

# Define the lifespan context manager: Initialize the database and import CSV data
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize database tables
    
    db = SessionLocal()
    try:
        # Read and insert CSV data
        df = pd.read_csv('healthcare_providers.csv')  # Update path as needed here

        for _, row in df.iterrows():
            # Check if provider already exists
            existing_provider = db.query(provider_models.Provider).filter(
                provider_models.Provider.name == row['name'],
                provider_models.Provider.specialty == row['specialty']
            ).first()
            if not existing_provider:
                provider = provider_models.Provider(
                    name=row['name'],
                    specialty=row['specialty']
                )
                db.add(provider)

        db.commit()
    finally:
        db.close()  # Ensure session closes after import

    yield  

# Pass the lifespan to FastAPI
app.router.lifespan_context = lifespan

# Root endpoint
@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to my Health Info System API. Visit /docs for documentation"}

# Include routers with prefixes
app.include_router(auth_routers.router, prefix="/auth", tags=["Auth"])
app.include_router(patient_routers.router, prefix="/patients", tags=["Patients"])
app.include_router(provider_routers.router, prefix="/providers", tags=["Providers"], dependencies=[Depends(get_current_user)])
app.include_router(appointment_routers.router, prefix="/appointments", tags=["Appointments"])