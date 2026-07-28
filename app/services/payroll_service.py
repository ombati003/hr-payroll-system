from datetime import datetime, date
import calendar
from app.models import Employee, PayrollRecord, db
from app.services.leave_service import LeaveService

class PayrollService:
    @staticmethod
    def calculate_monthly_payroll(employee_id, year, month):
        employee = Employee.query.get(employee_id)
        if not employee or employee.status != 'Active':
            return None

        # 1. Base Gross Pay
        monthly_salary = float(employee.salary)
        
        # 2. Handle Mid-month Joiners
        period_start = date(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        period_end = date(year, month, last_day)
        
        days_in_month = last_day
        work_days_count = days_in_month # Simplified to calendar days for this logic
        
        if employee.start_date > period_start:
            # Joined during the month
            effective_start = employee.start_date
            if effective_start > period_end:
                return None # Hasn't started yet
            worked_days = (period_end - effective_start).days + 1
            gross_pay = (monthly_salary / days_in_month) * worked_days
        else:
            gross_pay = monthly_salary

        # 3. Unpaid Leave Deduction
        unpaid_days = LeaveService.get_unpaid_leave_days(employee_id, period_start, period_end)
        unpaid_deduction = (monthly_salary / days_in_month) * unpaid_days
        gross_pay -= unpaid_deduction

        # 4. Statutory Deductions
        # Social Security: Flat 5%
        social_security = gross_pay * 0.05
        
        # Tax Brackets:
        # 0 - 2000: 0%
        # 2001 - 5000: 10%
        # 5001+: 20%
        taxable_income = gross_pay
        tax = 0
        if taxable_income > 5000:
            tax += (taxable_income - 5000) * 0.20
            tax += (5000 - 2000) * 0.10
        elif taxable_income > 2000:
            tax += (taxable_income - 2000) * 0.10
        
        net_pay = gross_pay - social_security - tax

        return {
            'employee_id': employee_id,
            'period_start': period_start,
            'period_end': period_end,
            'gross_pay': round(gross_pay, 2),
            'tax_deduction': round(tax, 2),
            'social_security_deduction': round(social_security, 2),
            'unpaid_leave_deduction': round(unpaid_deduction, 2),
            'net_pay': round(net_pay, 2)
        }

    @staticmethod
    def generate_bulk_payroll(year, month):
        employees = Employee.query.filter_by(status='Active').all()
        results = []
        for emp in employees:
            payroll_data = PayrollService.calculate_monthly_payroll(emp.id, year, month)
            if payroll_data:
                # Check if record already exists
                existing = PayrollRecord.query.filter_by(
                    employee_id=emp.id,
                    period_start=payroll_data['period_start']
                ).first()
                
                if not existing:
                    record = PayrollRecord(**payroll_data)
                    db.session.add(record)
                    results.append(record)
        
        db.session.commit()
        return results
