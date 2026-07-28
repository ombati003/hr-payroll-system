from flask import Blueprint, request, jsonify
from app import db
from app.models import Employee, Team
from datetime import datetime

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([e.to_dict() for e in employees])

@employees_bp.route('/', methods=['POST'])
def create_employee():
    data = request.json
    try:
        new_employee = Employee(
            name=data['name'],
            email=data['email'],
            role=data['role'],
            team_id=data.get('team_id'),
            manager_id=data.get('manager_id'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            salary=data['salary'],
            employment_type=data['employment_type']
        )
        db.session.add(new_employee)
        db.session.commit()
        return jsonify(new_employee.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@employees_bp.route('/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.json
    try:
        employee.name = data.get('name', employee.name)
        employee.email = data.get('email', employee.email)
        employee.role = data.get('role', employee.role)
        employee.team_id = data.get('team_id', employee.team_id)
        employee.manager_id = data.get('manager_id', employee.manager_id)
        if 'start_date' in data:
            employee.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        employee.salary = data.get('salary', employee.salary)
        employee.employment_type = data.get('employment_type', employee.employment_type)
        employee.status = data.get('status', employee.status)
        
        db.session.commit()
        return jsonify(employee.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@employees_bp.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([t.to_dict() for t in teams])

@employees_bp.route('/teams', methods=['POST'])
def create_team():
    data = request.json
    try:
        new_team = Team(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(new_team)
        db.session.commit()
        return jsonify(new_team.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
