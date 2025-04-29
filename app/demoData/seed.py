import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session, init_db
from app.controllers.user_controller import create_user
from app.controllers.patient_controller import create_patient
from app.controllers.appointment_controller import create_appointment
from app.controllers.prescription_controller import create_prescription
from app.schemas.user import UserCreate
from app.schemas.patient import PatientCreate
from app.schemas.appointment import AppointmentCreate
from app.schemas.prescription import PrescriptionCreate
from datetime import datetime, timedelta, date
import random

async def seed_data():
    """
    Seed the database with demo data
    """
    print("Initializing database...")
    await init_db()
    
    async with async_session() as db:
        # Create admin user
        admin_user = UserCreate(
            email="admin@healthcare.com",
            username="admin",
            password="Admin123!",
            full_name="Admin User",
            is_admin=True
        )
        admin = await create_user(db, admin_user)
        print(f"Created admin user: {admin.username}")
        
        # Create doctor users
        doctors = []
        for i in range(1, 4):
            doctor = UserCreate(
                email=f"doctor{i}@healthcare.com",
                username=f"doctor{i}",
                password=f"Doctor{i}123!",
                full_name=f"Doctor {i}",
                is_admin=False
            )
            db_doctor = await create_user(db, doctor)
            doctors.append(db_doctor)
            print(f"Created doctor: {db_doctor.username}")
        
        # Create patients for each doctor
        patients = []
        genders = ["Male", "Female", "Other"]
        
        for doctor in doctors:
            for i in range(1, 6):  # 5 patients per doctor
                patient = PatientCreate(
                    first_name=f"Patient{i}",
                    last_name=f"For{doctor.username}",
                    date_of_birth=date(1980 + i, i, i),
                    gender=random.choice(genders),
                    contact_number=f"+1234567890{i}",
                    email=f"patient{i}_{doctor.username}@example.com",
                    address=f"{i} Medical Street, Healthcare City",
                    medical_history=f"Patient {i} medical history for {doctor.username}",
                    doctor_id=doctor.id
                )
                db_patient = await create_patient(db, patient)
                patients.append(db_patient)
                print(f"Created patient: {db_patient.first_name} {db_patient.last_name}")
        
        # Create appointments
        now = datetime.now()
        
        for patient in patients:
            # Past appointment
            past_date = now - timedelta(days=random.randint(1, 30))
            past_appointment = AppointmentCreate(
                patient_id=patient.id,
                doctor_id=patient.doctor_id,
                appointment_date=past_date,
                reason=f"Regular checkup for {patient.first_name}",
                notes="Completed appointment"
            )
            await create_appointment(db, past_appointment)
            
            # Future appointment
            future_date = now + timedelta(days=random.randint(1, 30))
            future_appointment = AppointmentCreate(
                patient_id=patient.id,
                doctor_id=patient.doctor_id,
                appointment_date=future_date,
                reason=f"Follow-up for {patient.first_name}",
                notes="Scheduled appointment"
            )
            await create_appointment(db, future_appointment)
            
            print(f"Created appointments for patient: {patient.first_name} {patient.last_name}")
        
        # Create prescriptions
        medications = [
            "Amoxicillin 500mg",
            "Ibuprofen 400mg",
            "Paracetamol 500mg",
            "Omeprazole 20mg",
            "Simvastatin 40mg"
        ]
        
        diagnoses = [
            "Common Cold",
            "Hypertension",
            "Type 2 Diabetes",
            "Migraine",
            "Gastritis"
        ]
        
        for patient in patients:
            prescription = PrescriptionCreate(
                patient_id=patient.id,
                doctor_id=patient.doctor_id,
                diagnosis=random.choice(diagnoses),
                medications=random.choice(medications),
                instructions=f"Take twice daily after meals for {random.randint(5, 14)} days"
            )
            await create_prescription(db, prescription)
            print(f"Created prescription for patient: {patient.first_name} {patient.last_name}")
        
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())