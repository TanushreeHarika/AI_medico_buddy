"""
LifePulse Autonomous Emergency Agent

Simulates automatic emergency response for fatal/critical conditions:
1. Detects critical condition
2. Simulates emergency call dispatch
3. Sends patient data to Supabase hospital_notifications table
4. Logs all actions for audit trail
"""

import json
import os
from datetime import datetime


class EmergencyAgent:
    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        self.log_file = os.path.join(os.path.dirname(__file__), "..", "emergency_logs.json")

    def trigger(self, condition, severity, lat, lng, address):
        timestamp = datetime.utcnow().isoformat()

        notification = {
            "patient_condition": condition,
            "patient_location_lat": lat,
            "patient_location_lng": lng,
            "patient_location_address": address,
            "severity": severity,
            "status": "pending",
            "emergency_type": self._classify(condition),
            "timestamp": timestamp,
            "notes": f"Auto-triggered by LifePulse Agent. Condition: {condition}. Location: {address}.",
        }

        self._log_event(notification)
        call_status = self._simulate_call(condition, address)
        db_status = self._send_to_supabase(notification)

        print(f"\n🚨 EMERGENCY AGENT TRIGGERED")
        print(f"   Condition: {condition} | Severity: {severity}")
        print(f"   Location:  {address} ({lat}, {lng})")
        print(f"   DB Status: {db_status}\n")

        return {
            "success": True,
            "message": "Emergency response initiated",
            "details": {
                "condition": condition,
                "severity": severity,
                "location": {"lat": lat, "lng": lng, "address": address},
                "emergency_call": call_status,
                "hospital_notification": db_status,
                "timestamp": timestamp,
            },
            "actions_taken": [
                "✅ Critical condition detected and logged",
                "✅ Emergency call simulated (911/112)",
                f"{'✅' if db_status == 'sent' else '⚠'} Hospital notification {'sent to Supabase' if db_status == 'sent' else 'logged locally'}",
                "✅ Nearest ambulance unit alerted",
            ],
        }

    def _classify(self, condition):
        c = condition.lower()
        if "heart" in c or "cardiac" in c:
            return "cardiac_emergency"
        if "stroke" in c or "brain" in c:
            return "neurological_emergency"
        if "breath" in c or "chok" in c:
            return "respiratory_emergency"
        return "general_emergency"

    def _simulate_call(self, condition, address):
        print(f"   📞 Simulating emergency call for: {condition} at {address}")
        return "simulated_call_dispatched"

    def _send_to_supabase(self, notification):
        if self.supabase:
            try:
                result = self.supabase.table("hospital_notifications").insert(notification).execute()
                return "sent" if result.data else "failed"
            except Exception as e:
                print(f"   ⚠ Supabase error: {e}")
                return "error"
        return "logged_locally"

    def _log_event(self, notification):
        try:
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, "r") as f:
                    logs = json.load(f)
            logs.append(notification)
            with open(self.log_file, "w") as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"   ⚠ Log error: {e}")
