from flask import Blueprint, render_template

main_fe_bp = Blueprint('main_fe', __name__)

@main_fe_bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@main_fe_bp.route('/employees')
def employees():
    return render_template('employees.html')

@main_fe_bp.route('/teams')
def teams():
    return render_template('teams.html')

@main_fe_bp.route('/leave')
def leave():
    return render_template('leave.html')

@main_fe_bp.route('/payroll')
def payroll():
    return render_template('payroll.html')

@main_fe_bp.route('/payslips')
def payslips():
    return render_template('payroll.html') # Reusing payroll for payslips in this MVP

@main_fe_bp.route('/reports')
def reports():
    return render_template('dashboard.html') # Placeholder

@main_fe_bp.route('/settings')
def settings():
    return render_template('dashboard.html') # Placeholder
