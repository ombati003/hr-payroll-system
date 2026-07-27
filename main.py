from flask import Blueprint, jsonify
from app.models import Employee, LeaveRequest, PayrollRecord, Team
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/dashboard', methods=['GET'])
def get_dashboard_stats():
    today = datetime.utcnow().date()
    
    total_employees = Employee.query.filter_by(status='Active').count()
    on_leave_today = LeaveRequest.query.filter(
        LeaveRequest.start_date <= today,
        LeaveRequest.end_date >= today,
        LeaveRequest.status == 'Approved'
    ).count()
    pending_requests = LeaveRequest.query.filter_by(status='Pending').count()
    
    # Simple payroll stats for the current month
    current_month = today.month
    current_year = today.year
    monthly_payroll = db.session.query(db.func.sum(PayrollRecord.gross_pay)).filter(
        db.extract('month', PayrollRecord.period_start) == current_month,
        db.extract('year', PayrollRecord.period_start) == current_year
    ).scalar() or 0
    
    avg_salary = db.session.query(db.func.avg(Employee.salary)).filter_by(status='Active').scalar() or 0
    
    return jsonify({
        'total_employees': total_employees,
        'on_leave_today': on_leave_today,
        'pending_requests': pending_requests,
        'monthly_payroll': float(monthly_payroll),
        'avg_salary': float(avg_salary)
    })

# Add db import to this file as well
from app import db
