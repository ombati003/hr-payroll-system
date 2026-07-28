from datetime import datetime, timedelta
from app.models import LeaveRequest, Employee, db

class LeaveService:
    @staticmethod
    def validate_leave_request(employee_id, start_date, end_date, leave_type):
        """
        Validates leave request based on business rules:
        1. Notice period (at least 7 days for Annual leave)
        2. Team coverage (at least 50% of team must be present)
        """
        employee = Employee.query.get(employee_id)
        if not employee:
            return False, "Employee not found"

        start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
        today = datetime.utcnow().date()

        # Rule 1: Notice Period
        if leave_type == 'Annual' and (start_dt - today).days < 7:
            return False, "Annual leave requires at least 7 days notice."

        # Rule 2: Team Coverage
        if employee.team_id:
            team_members = Employee.query.filter_by(team_id=employee.team_id, status='Active').all()
            total_members = len(team_members)
            
            # Check how many team members are already on leave during this period
            overlapping_leaves = LeaveRequest.query.join(LeaveRequest.employee).filter(
                Employee.team_id == employee.team_id,
                LeaveRequest.status == 'Approved',
                LeaveRequest.start_date <= end_dt,
                LeaveRequest.end_date >= start_dt
            ).count()

            if (overlapping_leaves + 1) > (total_members / 2):
                return False, "Team coverage rule: At least 50% of the team must be present."

        return True, "Valid"

    @staticmethod
    def get_unpaid_leave_days(employee_id, start_date, end_date):
        """Calculates total unpaid leave days in a given period."""
        leaves = LeaveRequest.query.filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.leave_type == 'Unpaid',
            LeaveRequest.status == 'Approved',
            LeaveRequest.start_date <= end_date,
            LeaveRequest.end_date >= start_date
        ).all()

        total_days = 0
        for leave in leaves:
            # Calculate intersection of leave period and target period
            actual_start = max(leave.start_date, start_date)
            actual_end = min(leave.end_date, end_date)
            days = (actual_end - actual_start).days + 1
            total_days += days
        
        return total_days
