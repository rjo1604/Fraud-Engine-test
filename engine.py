from enum import Enum
from typing import Any, Dict, List


class Field:
    def of(self, row: Dict[str, Any]) -> Any:
        return row[self.value]

# Change *Field classes to match
# fields in the database table
class DataField(Field, Enum):
    Stops = 'stops'
    Location = 'location'
    ApplicationUpdates = 'application_updates'
    ScheduledLocations = 'scheduled_locations'
    DelinquentLocations = 'delinquent_locations'
    Payments = 'payments'
    Reports = 'reports'


class StopField(Field, Enum):
    Location = 'location'
    LocationState = 'location_data'

class ReportField(Field, Enum):
    Report = 'report'

class PaymentField(Field, Enum):
    Collected = 'collected'


class FraudDetectionEngine:
    def __init__(self):
        self.rules = (
            ('Stop location does not match scheduled location!', self.rule_stop_location_matches_scheduled),
            ('Location data is switch off!', self.rule_location_data_off),
            ('Data updated for customer at a different location than the scheduled point!', self.rule_application_updates_mismatch),
            ('Stop at a Delinquent location!', self.rule_delinquent_location_visited),
            ('Payment not collected from customer!', self.rule_uncollected_payments),
            ('Pattern Detected- Repeated PTP requests!', self.rule_repeated_ptp_reports)
        )

    def evaluate_rules(self, data) -> List[str]:
        alerts = []
        for rule_name, rule_function in self.rules:
            if rule_function(data):
                alerts.append(f"ALERT: {rule_name}")
        return alerts
    
    #Defining the Rules
    
    #Does the stop location match with scheduled collection location?
    def rule_stop_location_matches_scheduled(self, data) -> bool:
        stops = DataField.Stops.of(data)
        scheduled_locations = DataField.ScheduledLocations.of(data)
        return any(StopField.Location.of(stop) not in scheduled_locations for stop in stops)
    
    #Was the location data switched off deliberately?
    def rule_location_data_off(self, data) -> bool:
        stops = DataField.Stops.of(data)
        return any(StopField.LocationState.of(stop) == 'off' for stop in stops)
    
    #Was data updated for customer at a different location than the scheduled point?
    def rule_application_updates_mismatch(self, data) -> bool:
        stops = DataField.Stops.of(data)
        application_updates = DataField.ApplicationUpdates.of(data)
        return any(StopField.Location.of(stop) in application_updates for stop in stops)
    
    #Does the stop location match with recent delinquent or closed customer locations?
    def rule_delinquent_location_visited(self, data) -> bool:
        stops = DataField.Stops.of(data)
        delinquent_locations = DataField.DelinquentLocations.of(data)
        return any(StopField.Location.of(stop) in delinquent_locations for stop in stops)
    
    #Was the payment collected from the customer?
    def rule_uncollected_payments(self, data) -> bool:
        payments = DataField.Payments.of(data)
        return any(not PaymentField.Collected.of(payment) for payment in payments)
    
    #Is there a certain pattern in reporting PTP by the field officer?
    def rule_repeated_ptp_reports(self, data) -> bool:
        reports = DataField.Reports.of(data)
        ptp_count = 0
        for report in reports:
            if 'PTP reported' in ReportField.Report.of(report):
                ptp_count += 1
            if ptp_count > 3:  # Change this threshold as needed
                return True
        return False
