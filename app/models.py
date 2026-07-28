from datetime import datetime
from app import db

# class Team(db.Model):
#     __tablename__ = 'teams'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True, nullable=False)
#     description = db.Column(db.String(256))
#     employees = db.relationship('Employee', backref='team', lazy='dynamic')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description
#         }

# class Employee(db.Model):
#     __tablename__ = 'employees'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     role = db.Column(db.String(64), nullable=False)
#     team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
#     manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
#     start_date = db.Column(db.Date, nullable=False)
#     salary = db.Column(db.Numeric(12, 2), nullable=False)
#     employment_type = db.Column(db.String(32), nullable=False) # Full-time, Part-time, Contract
#     status = db.Column(db.String(16), default='Active') # Active, Inactive
    
#     # Relationships
#     subordinates = db.relationship('Employee', backref=db.backref('manager', remote_side=[id]), lazy='dynamic')
#     leave_requests = db.relationship('LeaveRequest', backref='employee', lazy='dynamic')
#     payroll_records = db.relationship('PayrollRecord', backref='employee', lazy='dynamic')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'email': self.email,
#             'role': self.role,
#             'team': self.team.name if self.team else None,
#             'team_id': self.team_id,
#             'manager': self.manager.name if self.manager else None,
#             'manager_id': self.manager_id,
#             'start_date': self.start_date.isoformat() if self.start_date else None,
#             'salary': float(self.salary),
#             'employment_type': self.employment_type,
#             'status': self.status
#         }

# class LeaveRequest(db.Model):
#     __tablename__ = 'leave_requests'
#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
#     leave_type = db.Column(db.String(32), nullable=False) # Annual, Sick, Unpaid
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=False)
#     status = db.Column(db.String(16), default='Pending') # Pending, Approved, Rejected
#     reason = db.Column(db.Text)
#     approved_by = db.Column(db.Integer, db.ForeignKey('employees.id'))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'employee_name': self.employee.name,
#             'employee_id': self.employee_id,
#             'leave_type': self.leave_type,
#             'start_date': self.start_date.isoformat(),
#             'end_date': self.end_date.isoformat(),
#             'status': self.status,
#             'reason': self.reason,
#             'created_at': self.created_at.isoformat()
#         }

# class PayrollRecord(db.Model):
#     __tablename__ = 'payroll_records'
#     id = db.Column(db.Integer, primary_key=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
#     period_start = db.Column(db.Date, nullable=False)
#     period_end = db.Column(db.Date, nullable=False)
#     gross_pay = db.Column(db.Numeric(12, 2), nullable=False)
#     tax_deduction = db.Column(db.Numeric(12, 2), nullable=False)
#     social_security_deduction = db.Column(db.Numeric(12, 2), nullable=False)
#     unpaid_leave_deduction = db.Column(db.Numeric(12, 2), nullable=False)
#     net_pay = db.Column(db.Numeric(12, 2), nullable=False)
#     status = db.Column(db.String(16), default='Draft') # Draft, Finalized
#     generated_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'employee_name': self.employee.name,
#             'employee_id': self.employee_id,
#             'period_start': self.period_start.isoformat(),
#             'period_end': self.period_end.isoformat(),
#             'gross_pay': float(self.gross_pay),
#             'tax_deduction': float(self.tax_deduction),
#             'social_security_deduction': float(self.social_security_deduction),
#             'unpaid_leave_deduction': float(self.unpaid_leave_deduction),
#             'net_pay': float(self.net_pay),
#             'status': self.status,
#             'generated_at': self.generated_at.isoformat()
#         }





class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))

    employees = db.relationship(
        "Employee",
        back_populates="team",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "employee_count": len(self.employees)
        }


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(64), nullable=False)

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))

    manager_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=True
    )

    start_date = db.Column(db.Date, nullable=False)

    salary = db.Column(db.Numeric(12,2), nullable=False)

    employment_type = db.Column(db.String(32), nullable=False)

    status = db.Column(db.String(16), default="Active")


    # -------------------------
    # Relationships
    # -------------------------

    team = db.relationship(
        "Team",
        back_populates="employees"
    )

    manager = db.relationship(
        "Employee",
        remote_side=[id],
        back_populates="subordinates"
    )

    subordinates = db.relationship(
        "Employee",
        back_populates="manager",
        lazy=True
    )

    leave_requests = db.relationship(
        "LeaveRequest",
        foreign_keys="LeaveRequest.employee_id",
        back_populates="employee",
        lazy=True
    )

    approved_leaves = db.relationship(
        "LeaveRequest",
        foreign_keys="LeaveRequest.approved_by",
        back_populates="approver",
        lazy=True
    )

    payroll_records = db.relationship(
        "PayrollRecord",
        foreign_keys="PayrollRecord.employee_id",
        back_populates="employee",
        lazy=True
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'team': self.team.name if self.team else None,
            'team_id': self.team_id,
            'manager': self.manager.name if self.manager else None,
            'manager_id': self.manager_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'salary': float(self.salary),
            'employment_type': self.employment_type,
            'status': self.status
        }

class LeaveRequest(db.Model):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    approved_by = db.Column(
        db.Integer,
        db.ForeignKey("employees.id")
    )

    leave_type = db.Column(db.String(32), nullable=False)

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(16), default="Pending")

    reason = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    employee = db.relationship(
        "Employee",
        foreign_keys=[employee_id],
        back_populates="leave_requests"
    )

    approver = db.relationship(
        "Employee",
        foreign_keys=[approved_by],
        back_populates="approved_leaves"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'employee_name': self.employee.name,
            'employee_id': self.employee_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }


class PayrollRecord(db.Model):
    __tablename__ = "payroll_records"

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False
    )

    period_start = db.Column(db.Date, nullable=False)

    period_end = db.Column(db.Date, nullable=False)

    gross_pay = db.Column(db.Numeric(12,2), nullable=False)

    tax_deduction = db.Column(db.Numeric(12,2), nullable=False)

    social_security_deduction = db.Column(db.Numeric(12,2), nullable=False)

    unpaid_leave_deduction = db.Column(db.Numeric(12,2), nullable=False)

    net_pay = db.Column(db.Numeric(12,2), nullable=False)

    status = db.Column(db.String(16), default="Draft")

    generated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    employee = db.relationship(
        "Employee",
        foreign_keys=[employee_id],
        back_populates="payroll_records"
    )

    def to_dict(self):
        return {
            'id': self.id,
            'employee_name': self.employee.name,
            'employee_id': self.employee_id,
            'period_start': self.period_start.isoformat(),
            'period_end': self.period_end.isoformat(),
            'gross_pay': float(self.gross_pay),
            'tax_deduction': float(self.tax_deduction),
            'social_security_deduction': float(self.social_security_deduction),
            'unpaid_leave_deduction': float(self.unpaid_leave_deduction),
            'net_pay': float(self.net_pay),
            'status': self.status,
            'generated_at': self.generated_at.isoformat()
        }

