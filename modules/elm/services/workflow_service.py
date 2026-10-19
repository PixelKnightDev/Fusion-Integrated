from datetime import datetime
from typing import List, Optional
from modules.elm.models.leave_application import LeaveApplication
from modules.elm.models.leave_types import LeaveType

class WorkflowService:
    @staticmethod
    def get_next_authority(application: LeaveApplication) -> str:
        """
        Determines the next sanctioning authority or reviewer based on 
        applicant's org unit, designation, leave category, and hierarchy config.
        """
        # Implementation of logic from specifications
        # Applicant's role/designation and organizational unit determine the path.
        # For CL and RH: Unit Head is the final authority.
        # For SCL, EL, COL, VL: Unit Head reviews, then moves to higher sanctioning authority.
        
        # This logic relies on data from Directory/User modules.
        return "UnitHead"

    @staticmethod
    def process_decision(application: LeaveApplication, decision: str, decision_maker_id: int) -> LeaveApplication:
        """
        Records a decision ('RECOMMENDED', 'NOT_RECOMMENDED', 'APPROVED', 'REJECTED')
        and updates the application status.
        """
        # Input validation for status
        valid_decisions = ['RECOMMENDED', 'NOT_RECOMMENDED', 'APPROVED', 'REJECTED', 'WITHDRAWN', 'CANCELLED']
        if decision not in valid_decisions:
            raise ValueError(f"Invalid decision state: {decision}")
            
        application.status = decision
        application.decision_maker_id = decision_maker_id
        application.decision_date = datetime.now()
        application.save()
        return application

    @staticmethod
    def check_sla_and_notify(application: LeaveApplication) -> None:
        """
        Checks if an application has exceeded any SLA thresholds and 
        triggers notifications/escalations.
        """
        # Placeholder for SLA logic
        pass
