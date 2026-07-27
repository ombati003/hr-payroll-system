from flask import Blueprint, request, jsonify
from app import db
from app.models import LeaveRequest, Employee
from app.services.leave_service import LeaveService
from datetime import datetime

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/', methods=['GET'])
def get_leaves():
    status = request.args.get('status')
    query = LeaveRequest.query
    if status:
        query = query.filter_by(status=status)
    leaves = query.order_by(LeaveRequest.created_at.desc()).all()
    return jsonify([l.to_dict() for l in leaves])

@leave_bp.route('/', methods=['POST'])
def create_leave():
    data = request.json
    is_valid, message = LeaveService.validate_leave_request(
        data['employee_id'], data['start_date'], data['end_date'], data['leave_type']
    )
    
    if not is_valid:
        return jsonify({'error': message}), 400

    try:
        new_leave = LeaveRequest(
            employee_id=data['employee_id'],
            leave_type=data['leave_type'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            reason=data.get('reason'),
            status='Pending'
        )
        db.session.add(new_leave)
        db.session.commit()
        return jsonify(new_leave.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@leave_bp.route('/<int:id>/approve', methods=['POST'])
def approve_leave(id):
    leave = LeaveRequest.query.get_or_404(id)
    data = request.json
    leave.status = 'Approved'
    leave.approved_by = data.get('approved_by')
    db.session.commit()
    return jsonify(leave.to_dict())

@leave_bp.route('/<int:id>/reject', methods=['POST'])
def reject_leave(id):
    leave = LeaveRequest.query.get_or_404(id)
    leave.status = 'Rejected'
    db.session.commit()
    return jsonify(leave.to_dict())
