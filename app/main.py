from fastapi import Depends, FastAPI
from app.dependencies import get_current_user
from app.routers import appointment_routers, auth_routers, medication_routers, patient_routers, provider_routers
from app.db.session import init_db

# Create FastAPI instance
app = FastAPI(
    title="Health Info System API",
)

# Initialize the database tables
init_db()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Health Info System API"}

# Include routers with prefixes
app.include_router(auth_routers.router, prefix="/auth", tags=["Auth"])
app.include_router(patient_routers.router, prefix="/patients", tags=["Patients"], dependencies=[Depends(get_current_user)])
app.include_router(provider_routers.router, prefix="/providers", tags=["Providers"])
app.include_router(appointment_routers.router, prefix="/appointments", tags=["Appointments"])
app.include_router(medication_routers.router, prefix="/medications", tags=["Medications"])
