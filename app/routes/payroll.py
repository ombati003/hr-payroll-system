from flask import Blueprint, request, jsonify
from app import db
from app.models import PayrollRecord, Employee
from app.services.payroll_service import PayrollService
from datetime import datetime

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/', methods=['GET'])
def get_payroll_history():
    employee_id = request.args.get('employee_id')
    query = PayrollRecord.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    records = query.order_by(PayrollRecord.period_start.desc()).all()
    return jsonify([r.to_dict() for r in records])

@payroll_bp.route('/generate', methods=['POST'])
def generate_payroll():
    data = request.json
    year = data.get('year', datetime.utcnow().year)
    month = data.get('month', datetime.utcnow().month)
    
    records = PayrollService.generate_bulk_payroll(year, month)
    return jsonify({
        'message': f'Generated {len(records)} payroll records.',
        'records': [r.to_dict() for r in records]
    })

@payroll_bp.route('/<int:id>', methods=['GET'])
def get_payslip(id):
    record = PayrollRecord.query.get_or_404(id)
    return jsonify(record.to_dict())

@payroll_bp.route('/<int:id>/finalize', methods=['POST'])
def finalize_payroll(id):
    record = PayrollRecord.query.get_or_404(id)
    record.status = 'Finalized'
    db.session.commit()
    return jsonify(record.to_dict())
