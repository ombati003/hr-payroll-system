import pytest
from datetime import date
from app import create_app, db
from app.models import Employee, Team, LeaveRequest
from app.services.payroll_service import PayrollService
from app.services.leave_service import LeaveService
from config import Config

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_payroll_calculation(app):
    with app.app_context():
        # Create a test employee
        emp = Employee(
            name="Test User",
            email="test@example.com",
            role="Dev",
            start_date=date(2023, 1, 1),
            salary=6000,
            employment_type="Full-time"
        )
        db.session.add(emp)
        db.session.commit()

        # Calculate payroll for July 2026
        result = PayrollService.calculate_monthly_payroll(emp.id, 2026, 7)
        
        # Gross: 6000
        # SS (5%): 300
        # Tax: (6000-5000)*0.2 + (5000-2000)*0.1 = 200 + 300 = 500
        # Net: 6000 - 300 - 500 = 5200
        
        assert result['gross_pay'] == 6000.0
        assert result['social_security_deduction'] == 300.0
        assert result['tax_deduction'] == 500.0
        assert result['net_pay'] == 5200.0

def test_mid_month_joiner(app):
    with app.app_context():
        # Joins on July 16th (July has 31 days)
        emp = Employee(
            name="New Joiner",
            email="new@example.com",
            role="Dev",
            start_date=date(2026, 7, 16),
            salary=3100,
            employment_type="Full-time"
        )
        db.session.add(emp)
        db.session.commit()

        result = PayrollService.calculate_monthly_payroll(emp.id, 2026, 7)
        
        # Worked 16 days (16th to 31st)
        # Gross: (3100 / 31) * 16 = 1600
        # SS (5%): 80
        # Tax: 0 (Below 2000)
        # Net: 1520
        
        assert result['gross_pay'] == 1600.0
        assert result['net_pay'] == 1520.0

def test_leave_notice_rule(app):
    with app.app_context():
        emp = Employee(
            name="Leave User",
            email="leave@example.com",
            role="Dev",
            start_date=date(2023, 1, 1),
            salary=3000,
            employment_type="Full-time"
        )
        db.session.add(emp)
        db.session.commit()

        # Current date in simulation is 2026-07-27 (from system prompt)
        # Try to request leave for tomorrow (2026-07-28)
        is_valid, msg = LeaveService.validate_leave_request(emp.id, "2026-07-28", "2026-07-30", "Annual")
        assert is_valid is False
        assert "7 days notice" in msg

def test_team_coverage_rule(app):
    with app.app_context():
        team = Team(name="Engineering")
        db.session.add(team)
        db.session.commit()

        # Create 2 employees in the team
        e1 = Employee(name="E1", email="e1@ex.com", role="D", team_id=team.id, start_date=date(2023,1,1), salary=1, employment_type="F")
        e2 = Employee(name="E2", email="e2@ex.com", role="D", team_id=team.id, start_date=date(2023,1,1), salary=1, employment_type="F")
        db.session.add_all([e1, e2])
        db.session.commit()

        # E1 has approved leave
        l1 = LeaveRequest(employee_id=e1.id, start_date=date(2026,8,1), end_date=date(2026,8,5), status='Approved', leave_type='Annual')
        db.session.add(l1)
        db.session.commit()

        # E2 tries to request leave for same period
        is_valid, msg = LeaveService.validate_leave_request(e2.id, "2026-08-02", "2026-08-03", "Annual")
        assert is_valid is False
        assert "50% of the team" in msg
