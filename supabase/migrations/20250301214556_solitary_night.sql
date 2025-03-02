/*
  # Initial schema for Healthcare API

  1. New Tables
    - `users`
      - `id` (uuid, primary key)
      - `email` (text, unique)
      - `full_name` (text)
      - `hashed_password` (text)
      - `is_active` (boolean)
      - `is_admin` (boolean)
      - `avatar_url` (text, nullable)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    - `patients`
      - `id` (uuid, primary key)
      - `first_name` (text)
      - `last_name` (text)
      - `date_of_birth` (timestamptz)
      - `gender` (text)
      - `phone_number` (text)
      - `address` (text, nullable)
      - `email` (text, nullable)
      - `blood_type` (text, nullable)
      - `allergies` (text, nullable)
      - `medical_history` (text, nullable)
      - `created_by` (uuid, foreign key to users)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    - `appointments`
      - `id` (uuid, primary key)
      - `patient_id` (uuid, foreign key to patients)
      - `doctor_id` (uuid, foreign key to users)
      - `appointment_date` (timestamptz)
      - `reason` (text)
      - `status` (text)
      - `notes` (text, nullable)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    - `prescriptions`
      - `id` (uuid, primary key)
      - `patient_id` (uuid, foreign key to patients)
      - `doctor_id` (uuid, foreign key to users)
      - `diagnosis` (text)
      - `notes` (text, nullable)
      - `file_url` (text, nullable)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)
    - `medications`
      - `id` (uuid, primary key)
      - `prescription_id` (uuid, foreign key to prescriptions)
      - `name` (text)
      - `dosage` (text)
      - `frequency` (text)
      - `duration` (text)
      - `instructions` (text, nullable)

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users
*/

-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  hashed_password TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  is_admin BOOLEAN NOT NULL DEFAULT FALSE,
  avatar_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  date_of_birth TIMESTAMPTZ NOT NULL,
  gender TEXT NOT NULL,
  phone_number TEXT NOT NULL,
  address TEXT,
  email TEXT,
  blood_type TEXT,
  allergies TEXT,
  medical_history TEXT,
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create appointments table
CREATE TABLE IF NOT EXISTS appointments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  doctor_id UUID NOT NULL REFERENCES users(id),
  appointment_date TIMESTAMPTZ NOT NULL,
  reason TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'scheduled',
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  patient_id UUID NOT NULL REFERENCES patients(id),
  doctor_id UUID NOT NULL REFERENCES users(id),
  diagnosis TEXT NOT NULL,
  notes TEXT,
  file_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Create medications table
CREATE TABLE IF NOT EXISTS medications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prescription_id UUID NOT NULL REFERENCES prescriptions(id),
  name TEXT NOT NULL,
  dosage TEXT NOT NULL,
  frequency TEXT NOT NULL,
  duration TEXT NOT NULL,
  instructions TEXT
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE prescriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE medications ENABLE ROW LEVEL SECURITY;

-- Create policies for users table
CREATE POLICY "Users can view their own data" 
  ON users 
  FOR SELECT 
  TO authenticated 
  USING (auth.uid() = id);

CREATE POLICY "Users can update their own data" 
  ON users 
  FOR UPDATE 
  TO authenticated 
  USING (auth.uid() = id);

CREATE POLICY "Admins can view all users" 
  ON users 
  FOR SELECT 
  TO authenticated 
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

CREATE POLICY "Admins can update all users" 
  ON users 
  FOR UPDATE 
  TO authenticated 
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

CREATE POLICY "Admins can delete users" 
  ON users 
  FOR DELETE 
  TO authenticated 
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

-- Create policies for patients table
CREATE POLICY "Authenticated users can view patients" 
  ON patients 
  FOR SELECT 
  TO authenticated 
  USING (TRUE);

CREATE POLICY "Authenticated users can create patients" 
  ON patients 
  FOR INSERT 
  TO authenticated 
  WITH CHECK (TRUE);

CREATE POLICY "Authenticated users can update patients" 
  ON patients 
  FOR UPDATE 
  TO authenticated 
  USING (TRUE);

CREATE POLICY "Admins can delete patients" 
  ON patients 
  FOR DELETE 
  TO authenticated 
  USING (
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

-- Create policies for appointments table
CREATE POLICY "Doctors can view their appointments" 
  ON appointments 
  FOR SELECT 
  TO authenticated 
  USING (doctor_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

CREATE POLICY "Authenticated users can create appointments" 
  ON appointments 
  FOR INSERT 
  TO authenticated 
  WITH CHECK (TRUE);

CREATE POLICY "Doctors can update their appointments" 
  ON appointments 
  FOR UPDATE 
  TO authenticated 
  USING (doctor_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

CREATE POLICY "Doctors can delete their appointments" 
  ON appointments 
  FOR DELETE 
  TO authenticated 
  USING (doctor_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

-- Create policies for prescriptions table
CREATE POLICY "Doctors can view their prescriptions" 
  ON prescriptions 
  FOR SELECT 
  TO authenticated 
  USING (doctor_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

CREATE POLICY "Authenticated users can create prescriptions" 
  ON prescriptions 
  FOR INSERT 
  TO authenticated 
  WITH CHECK (TRUE);

CREATE POLICY "Doctors can update their prescriptions" 
  ON prescriptions 
  FOR UPDATE 
  TO authenticated 
  USING (doctor_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

CREATE POLICY "Doctors can delete their prescriptions" 
  ON prescriptions 
  FOR DELETE 
  TO authenticated 
  USING (doctor_id = auth.uid() OR 
    EXISTS (
      SELECT 1 FROM users 
      WHERE users.id = auth.uid() 
      AND users.is_admin = TRUE
    )
  );

-- Create policies for medications table
CREATE POLICY "Authenticated users can view medications" 
  ON medications 
  FOR SELECT 
  TO authenticated 
  USING (TRUE);

CREATE POLICY "Authenticated users can create medications" 
  ON medications 
  FOR INSERT 
  TO authenticated 
  WITH CHECK (TRUE);

CREATE POLICY "Authenticated users can update medications" 
  ON medications 
  FOR UPDATE 
  TO authenticated 
  USING (TRUE);

CREATE POLICY "Authenticated users can delete medications" 
  ON medications 
  FOR DELETE 
  TO authenticated 
  USING (TRUE);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_patients_created_by ON patients(created_by);
CREATE INDEX IF NOT EXISTS idx_appointments_patient_id ON appointments(patient_id);
CREATE INDEX IF NOT EXISTS idx_appointments_doctor_id ON appointments(doctor_id);
CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);
CREATE INDEX IF NOT EXISTS idx_prescriptions_patient_id ON prescriptions(patient_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_doctor_id ON prescriptions(doctor_id);
CREATE INDEX IF NOT EXISTS idx_medications_prescription_id ON medications(prescription_id);