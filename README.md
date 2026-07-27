HR & Payroll Management System

Project Overview

This project implements a small internal HR & Payroll tool designed to manage employee records, leave requests, and payroll processing. It addresses common challenges faced by growing teams that rely on manual processes, such as lost approvals and incorrect payroll calculations. The system is built with a Python Flask backend, PostgreSQL database, and a modern HTML/CSS/JavaScript frontend, adhering to the provided Figma design.

Table of Contents

1.
Features

2.
Prioritization and Design Choices

3.
Technical Stack

4.
Database Schema

5.
Business Logic

•
Leave Management Rules

•
Payroll Formula



6.
Frontend Overview

7.
How to Run Locally

8.
Testing

9.
Future Improvements / Stretch Goals

Features

1. Employee Records

•
Employee Profiles: Stores essential information including name, role, team, manager, start date, salary, and employment type.

•
Organizational View: Provides a simple hierarchy showing who reports to whom.

•
Deactivation, Not Deletion: Employees can be deactivated to preserve payroll history, rather than being permanently deleted.

2. Leave Management

•
Request System: Employees can submit time-off requests.

•
Approval Workflow: Managers can approve or reject leave requests.

•
Intelligent Rules: Incorporates safeguards to prevent common issues:

•
Notice Period: Enforces a minimum notice period for certain leave types (e.g., annual leave).

•
Team Coverage: Ensures adequate team coverage by preventing too many team members from being on leave simultaneously.

•
Payroll Interaction: Unpaid leave automatically impacts payroll calculations.



3. Payroll

•
Monthly Payslip Generation: Generates detailed monthly payslips for each employee.

•
Gross Pay Calculation: Includes pro-ration for mid-month joiners and deductions for unpaid leave.

•
Statutory Deductions: Applies simplified tax brackets and a flat social security scheme.

•
Edge Case Handling: Manages scenarios like mid-month joiners and zero-deduction cases.

Prioritization and Design Choices

Given the broad scope, the development prioritized implementing the core business logic for Employee Records, Leave Management, and Payroll with robust rules and calculations. The frontend focuses on presenting this data clearly and providing necessary controls, closely following the provided Figma design for the dashboard, employee, and leave pages.

•
Backend First: Core business logic and data integrity were prioritized to ensure the system's foundation is sound.

•
Key Modules Over All Modules: Instead of shallowly implementing all three modules, a deeper implementation of Employee Records, Leave Management, and Payroll was chosen to demonstrate real business logic.

•
User Experience (UX) for Core Flows: The frontend for the dashboard, employee listing, and leave request/approval flows were given attention to ensure usability and adherence to the Figma design.

Technical Stack

•
Backend: Python 3.x with Flask framework.

•
Database: PostgreSQL, managed with SQLAlchemy ORM and Flask-Migrate for migrations.

•
Frontend: HTML5, CSS3 (using Tailwind CSS for utility-first styling), and Vanilla JavaScript for interactivity.

•
Dependencies: Managed via requirements/base.txt.

Database Schema

teams Table

Column Name
Type
Constraints
Description
id
INTEGER
PRIMARY KEY
Unique identifier for the team
name
VARCHAR(64)
UNIQUE, NOT NULL
Name of the team
description
VARCHAR(256)


Brief description of the team




employees Table

Column Name
Type
Constraints
Description
id
INTEGER
PRIMARY KEY
Unique identifier for the employee
name
VARCHAR(128)
NOT NULL
Full name of the employee
email
VARCHAR(120)
UNIQUE, NOT NULL
Employee's email address
role
VARCHAR(64)
NOT NULL
Employee's job role
team_id
INTEGER
FOREIGN KEY (teams.id)
ID of the team the employee belongs to
manager_id
INTEGER
FOREIGN KEY (employees.id)
ID of the employee's manager (self-referencing)
start_date
DATE
NOT NULL
Date when employment started
salary
NUMERIC(12,2)
NOT NULL
Monthly gross salary
employment_type
VARCHAR(32)
NOT NULL
Type of employment (e.g., Full-time, Part-time)
status
VARCHAR(16)
DEFAULT 'Active'
Employment status (Active, Inactive)




leave_requests Table

Column Name
Type
Constraints
Description
id
INTEGER
PRIMARY KEY
Unique identifier for the leave request
employee_id
INTEGER
FOREIGN KEY (employees.id), NOT NULL
Employee who requested leave
leave_type
VARCHAR(32)
NOT NULL
Type of leave (e.g., Annual, Sick, Unpaid)
start_date
DATE
NOT NULL
Start date of the leave
end_date
DATE
NOT NULL
End date of the leave
status
VARCHAR(16)
DEFAULT 'Pending'
Status of the request (Pending, Approved, Rejected)
reason
TEXT


Reason for the leave request
approved_by
INTEGER
FOREIGN KEY (employees.id)
Manager who approved the request
created_at
DATETIME
DEFAULT UTC_NOW
Timestamp of request creation




payroll_records Table

Column Name
Type
Constraints
Description
id
INTEGER
PRIMARY KEY
Unique identifier for the payroll record
employee_id
INTEGER
FOREIGN KEY (employees.id), NOT NULL
Employee for whom payroll is generated
period_start
DATE
NOT NULL
Start date of the payroll period
period_end
DATE
NOT NULL
End date of the payroll period
gross_pay
NUMERIC(12,2)
NOT NULL
Gross pay for the period
tax_deduction
NUMERIC(12,2)
NOT NULL
Tax deducted
social_security_deduction
NUMERIC(12,2)
NOT NULL
Social security deducted
unpaid_leave_deduction
NUMERIC(12,2)
NOT NULL
Deduction for unpaid leave
net_pay
NUMERIC(12,2)
NOT NULL
Net pay after all deductions
status
VARCHAR(16)
DEFAULT 'Draft'
Status of the payroll (Draft, Finalized)
generated_at
DATETIME
DEFAULT UTC_NOW
Timestamp of record generation




Business Logic

Leave Management Rules

•
Notice Period: For 'Annual' leave types, a request must be submitted at least 7 days before the start_date. This prevents last-minute disruptions.

•
Team Coverage: To ensure operational continuity, no more than 50% of a team's active members can be on approved leave during any overlapping period. This prevents a team from becoming understaffed.

•
Unpaid Leave & Payroll: Any approved 'Unpaid' leave days within a payroll period are automatically factored into the payroll calculation, leading to a pro-rated deduction from the gross pay.

Payroll Formula

•
Gross Pay: Calculated as Employee.salary (monthly base salary). For mid-month joiners, it's pro-rated based on the number of days worked in the month.

•
Daily Rate = Monthly Salary / Total Days in Month

•
Gross Pay (pro-rated) = Daily Rate * Days Worked



•
Unpaid Leave Deduction: If an employee has approved 'Unpaid' leave, the Daily Rate is multiplied by the number of unpaid leave days within the payroll period and deducted from the gross_pay.

•
Statutory Deductions:

•
Social Security: A flat 5% of the gross_pay.

•
Tax Brackets: A simplified progressive tax scheme is applied to the taxable_income (gross pay after social security deduction):

•
Up to $2000: 0%

•
$2001 - $5000: 10% on the amount over $2000

•
$5001 and above: 20% on the amount over $5000 (plus the 10% from the previous bracket)





•
Net Pay: Gross Pay - Social Security Deduction - Tax Deduction - Unpaid Leave Deduction.

Frontend Overview

The frontend is built using HTML, Tailwind CSS, and vanilla JavaScript to provide a responsive and interactive user interface, closely matching the Figma design. Key pages include:

•
Dashboard: Displays key HR metrics such as total employees, employees on leave today, pending leave requests, monthly payroll cost, and average salary. It also includes placeholders for monthly payroll cost charts and team distribution.

•
Employees: Lists all employees, allows adding new employees, and provides a basic organizational hierarchy view.

•
Teams: Displays a grid of teams and allows for the creation of new teams.

•
Leave Management: Shows pending leave requests, allows managers to approve/reject them, and enables employees to submit new leave requests. It also outlines the leave rules.

•
Payroll: Provides an interface to generate monthly payroll and view historical payroll records. It includes a modal for viewing detailed payslips.

How to Run Locally

Prerequisites

•
Python 3.8+

•
PostgreSQL

•
pip (Python package installer)

1. Clone the Repository

Bash


git clone <repository_url>
cd hr_payroll_system



2. Set up a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

Bash


python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate



3. Install Dependencies

Bash


pip install -r requirements/base.txt



4. Database Setup

a. Create PostgreSQL Database

Ensure you have a PostgreSQL server running. Create a database named hr_payroll (or as configured in config.py).

SQL


CREATE DATABASE hr_payroll;



b. Environment Variables

Create a .env file in the root directory of the project with your database connection string and a secret key:

Plain Text


DATABASE_URL="postgresql://your_user:your_password@localhost:5432/hr_payroll"
SECRET_KEY="your_super_secret_key"



Replace your_user and your_password with your PostgreSQL credentials.

c. Run Migrations

Initialize and apply database migrations:

Bash


flask db init
flask db migrate -m "Initial migration"
flask db upgrade



5. Run the Flask Application

Bash


python run.py



The application will be accessible at http://127.0.0.1:5000/.

Testing

Unit tests for core business logic, including payroll calculations and leave management rules, are located in the tests/ directory. To run tests:

Bash


pytest



Future Improvements / Stretch Goals

Given more time, the following improvements would enhance the system:

•
Authentication and Authorization: Implement a proper user authentication system (e.g., Flask-Login ) with role-based access control for managers and employees.

•
Detailed Reporting: Expand the reporting module with more comprehensive analytics and customizable reports (e.g., leave trends, payroll distribution by team).

•
Notifications: Implement real-time notifications for leave approvals/rejections, upcoming birthdays, and payroll generation.

•
UI Refinements: Further refine the frontend to exactly match all aspects of the Figma design, including interactive charts (e.g., using Chart.js or D3.js) and more polished empty/loading states.

•
Employee Self-Service Portal: Allow employees to view their own payslips, leave balances, and update personal information.

•
Admin Panel: A dedicated admin interface for managing system settings, user accounts, and global configurations.

•
API Documentation: Generate OpenAPI/Swagger documentation for the backend API endpoints.

•
Dockerization: Provide Docker support for easier deployment and environment consistency.

