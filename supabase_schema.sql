-- ============================================
-- LifePulse - Supabase Database Schema
-- Run this SQL in the Supabase SQL Editor
-- ============================================

-- Hospital Notifications Table
-- Stores emergency alerts sent by the Autonomous Agent
CREATE TABLE IF NOT EXISTS hospital_notifications (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  patient_condition TEXT NOT NULL,
  patient_location_lat DOUBLE PRECISION NOT NULL DEFAULT 0,
  patient_location_lng DOUBLE PRECISION NOT NULL DEFAULT 0,
  patient_location_address TEXT NOT NULL DEFAULT 'Unknown',
  severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'acknowledged', 'dispatched', 'resolved')),
  emergency_type TEXT NOT NULL DEFAULT 'general_emergency',
  timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE hospital_notifications ENABLE ROW LEVEL SECURITY;

-- Policy: Allow anonymous inserts (for emergency agent)
CREATE POLICY "Allow anonymous inserts" ON hospital_notifications
  FOR INSERT TO anon WITH CHECK (true);

-- Policy: Allow anonymous reads
CREATE POLICY "Allow anonymous reads" ON hospital_notifications
  FOR SELECT TO anon USING (true);

-- Index for fast queries
CREATE INDEX idx_notifications_timestamp ON hospital_notifications (timestamp DESC);
CREATE INDEX idx_notifications_severity ON hospital_notifications (severity);
CREATE INDEX idx_notifications_status ON hospital_notifications (status);
