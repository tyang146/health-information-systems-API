import unittest
from unittest.mock import MagicMock
from app.models import patient_models, appointment_models
from app.crud.appointment_crud import validate_appointment
from datetime import date, time, timedelta
from fastapi import HTTPException, status

class TestValidateAppointment(unittest.TestCase):
    def setUp(self):
        # Mock the database session
        self.mock_db = MagicMock()

        # Mock the Patient and Appointment models
        self.mock_patient = patient_models.Patient(id=1, name="John Doe")
        self.mock_appointment = appointment_models.Appointment(id=1, patient_id=1, provider_id=1, date=date.today(), time=time(10, 0))

    def test_validate_appointment_success(self):
        # Arrange: 
        self.mock_db.query.return_value.filter.return_value.all.return_value = [] # Simulate no conflicting appointments

        # Act:
        result = validate_appointment(self.mock_db, date.today(), time(11, 0), 1, 1)

        # Assert:
        self.assertIsNone(result) # No exception should be raised

    def test_validate_appointment_time_conflict(self):
        # Arrange: 
        self.mock_db.query.return_value.filter.return_value.all.return_value = [self.mock_appointment] # Simulate a conflicting appointment
        appointment_time = time(10, 30)  # This conflicts with the existing appointment at 10:00

        # Act & Assert: Expect an HTTPException due to the conflict
        with self.assertRaises(HTTPException) as context:
            validate_appointment(self.mock_db, date.today(), appointment_time, 1, 1)

        # Assert: Check that the exception message is correct
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "This patient already has an appointment scheduled around this time. Ensure appointments are at least 30 minutes apart.")

    def test_validate_appointment_in_past(self):
        # Arrange:
        appointment_date = date.today() - timedelta(days=1)  # Yesterday

        # Act & Assert: Check if HTTPException is raised for past appointment date
        with self.assertRaises(HTTPException) as context:
            validate_appointment(self.mock_db, appointment_date, time(10, 0), 1, 1)

        # Assert: Check that the exception message is correct
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "Appointment date cannot be set in the past.")

    def test_validate_appointment_time_outside_business_hours(self):
        # Arrange: 
        appointment_time = time(18, 0)  # 6:00 PM (outside business hours)

        # Act & Assert: Check if HTTPException is raised for time outside business hours
        with self.assertRaises(HTTPException) as context:
            validate_appointment(self.mock_db, date.today(), appointment_time, 1, 1)
            
        # Assert: Check that the exception message is correct
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "Appointments must be scheduled between 9:00 AM and 5:00 PM.")

    def test_validate_appointment_patient_not_found(self):
        # Arrange: Mock the patient query to return None
        self.mock_db.query.return_value.filter.return_value.first.return_value = None

        # Act & Assert: Check if HTTPException is raised for non-existing patient
        with self.assertRaises(HTTPException) as context:
            validate_appointment(self.mock_db, date.today(), time(10, 0), 999, 1)

        # Assert: Check that the exception message is correct
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Patient with ID 999 does not exist.")

    def test_validate_appointment_provider_not_found(self):
        # Arrange: Mock the patient query to return Patient but mock the provider query to return None 
        self.mock_db.query.return_value.filter.return_value.first.side_effect = self.mock_patient, None

        # Act & Assert: Check if HTTPException is raised for non-existing provider
        with self.assertRaises(HTTPException) as context:
            validate_appointment(self.mock_db, date.today(), time(10, 0), 1, 999)

        # Assert: Check that the exception message is correct
        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Provider with ID 999 does not exist.")

    def test_validate_provider_conflict(self):
        # Arrange: Mock successful patient appointment but conflicting provider appointment
        self.mock_db.query.return_value.filter.return_value.all.side_effect = None, self.mock_appointment

        # Act & Assert: Check if HTTPException is raised for conflicting provider appointments
        with self.assertRaises(HTTPException) as context:
            validate_appointment(self.mock_db, date.today(), time(10, 0), 1, 1)
            
        # Assert: Check that the exception message is correct
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, "An appointment already exists for this provider around this time. Choose a different time.")