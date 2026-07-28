# HR & Payroll Management System

## Project Overview

The **HR & Payroll Management System** is a modern web-based application designed to streamline Human Resource and Payroll operations for growing organizations. It eliminates the challenges of managing employee information, leave requests, and payroll calculations through spreadsheets and messaging platforms by providing a centralized, automated solution.

The system enables organizations to efficiently manage employee records, process leave requests through an approval workflow, and generate accurate monthly payrolls with statutory deductions and payslips. It is developed using a **Python Flask** backend, a **PostgreSQL** database, and a responsive **HTML, CSS, and JavaScript** frontend based on the provided Figma design.

---

# Table of Contents

- [Features](#features)
- [Project Prioritization and Design Choices](#project-prioritization-and-design-choices)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Business Logic](#business-logic)
  - [Leave Management Rules](#leave-management-rules)
  - [Payroll Formula](#payroll-formula)
- [Frontend Overview](#frontend-overview)
- [How to Run Locally](#how-to-run-locally)
- [Testing](#testing)
- [Future Improvements](#future-improvements)

---

# Features

The application consists of three primary modules.

## 1. Employee Records

The Employee Management module provides a centralized repository for all employee information.

### Key Features

| Feature | Description |
|----------|-------------|
| Employee Profiles | Stores employee name, role, team, manager, salary, employment type, and start date. |
| Organization Hierarchy | Displays reporting relationships between managers and employees. |
| Employee Status | Employees can be deactivated instead of permanently deleted to preserve payroll history. |

---

## 2. Leave Management

The Leave Management module automates the leave request and approval process.

### Key Features

| Feature | Description |
|----------|-------------|
| Leave Requests | Employees can submit leave applications directly through the system. |
| Approval Workflow | Managers can approve or reject leave requests. |
| Notice Period Validation | Enforces minimum notice periods for annual leave requests. |
| Team Coverage Validation | Prevents excessive leave requests that would leave teams understaffed. |
| Payroll Integration | Approved unpaid leave is automatically considered during payroll generation. |

---

## 3. Payroll Management

The Payroll module automatically generates employee payroll for each payroll period.

### Key Features

| Feature | Description |
|----------|-------------|
| Monthly Payslip Generation | Creates detailed payslips for every employee. |
| Gross Pay Calculation | Calculates monthly salary including pro-rated salaries for mid-month joiners. |
| Statutory Deductions | Applies predefined tax brackets and social security deductions. |
| Edge Case Handling | Handles zero deductions, salary boundary cases, and unpaid leave adjustments. |

---

# Project Prioritization and Design Choices

The project requirements intentionally provide a broad scope. Rather than implementing every feature superficially, the development focused on delivering robust business logic for the core HR operations.

The following priorities guided the implementation.

| Priority | Description |
|----------|-------------|
| Business Logic First | Payroll calculations and leave validation rules were prioritized over interface enhancements. |
| Core Modules | Employee Records, Leave Management, and Payroll were implemented with complete workflows rather than simple CRUD functionality. |
| Data Integrity | Soft deletion, relational database design, and validation rules ensure consistency of historical records. |
| User Experience | The frontend closely follows the supplied Figma design while maintaining simplicity and responsiveness. |

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Backend | Python 3.x |
| Framework | Flask |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Flask-Migrate |
| Frontend | HTML5 |
| Styling | CSS3 / Tailwind CSS |
| Client-side Scripting | Vanilla JavaScript |
| Package Management | pip |
| Dependencies | requirements/base.txt |

---

# Project Prioritization and Design Choices

Given the broad scope of the project, development focused on implementing robust business logic for the core HR functionalities rather than building every possible feature. The priority was to deliver a reliable system capable of managing employee records, processing leave requests, and generating accurate payroll while maintaining data integrity and a clean user experience.

The design decisions made throughout the project are summarized below.

| Design Choice | Description |
|---------------|-------------|
| **Backend First** | Core business logic, database relationships, and validation rules were prioritized to ensure the application's foundation is reliable and maintainable. |
| **Quality over Quantity** | Rather than implementing numerous incomplete features, development focused on delivering complete Employee Management, Leave Management, and Payroll modules with realistic business rules. |
| **Business Logic Driven** | The application emphasizes workflow automation, payroll calculations, leave validation, and organizational hierarchy instead of simple CRUD operations. |
| **User Experience** | The frontend follows the supplied Figma design to provide a clean, responsive, and intuitive interface for administrators, managers, and employees. |
| **Data Integrity** | Employees are deactivated instead of deleted, preserving payroll records and historical leave information. |
| **Scalable Architecture** | The project follows a modular Flask architecture with separate Blueprints, models, services, and templates to simplify future maintenance and feature expansion. |

---

# Technology Stack

The project utilizes modern web technologies to provide a scalable, responsive, and maintainable application.

| Layer | Technology |
|--------|------------|
| **Programming Language** | Python 3.x |
| **Backend Framework** | Flask |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Database Migrations** | Flask-Migrate |
| **Frontend** | HTML5 |
| **Styling** | CSS3 (Tailwind CSS) |
| **Client-side Scripting** | Vanilla JavaScript |
| **Package Management** | pip |
| **Dependency Management** | `requirements/base.txt` |

---

# Database Schema

The database is designed using a relational structure to maintain data consistency while supporting employee management, leave processing, and payroll generation.

---

## Teams Table

Stores information about organizational teams or departments.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the team |
| `name` | VARCHAR(64) | UNIQUE, NOT NULL | Name of the team |
| `description` | VARCHAR(256) | - | Brief description of the team |

---

## Employees Table

Stores employee information and reporting relationships.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the employee |
| `name` | VARCHAR(128) | NOT NULL | Full name of the employee |
| `email` | VARCHAR(120) | UNIQUE, NOT NULL | Employee email address |
| `role` | VARCHAR(64) | NOT NULL | Employee job role |
| `team_id` | INTEGER | FOREIGN KEY (`teams.id`) | Team the employee belongs to |
| `manager_id` | INTEGER | FOREIGN KEY (`employees.id`) | Employee's manager (self-reference) |
| `start_date` | DATE | NOT NULL | Employment start date |
| `salary` | NUMERIC(12,2) | NOT NULL | Monthly gross salary |
| `employment_type` | VARCHAR(32) | NOT NULL | Employment type (Full-time, Part-time, Contract, etc.) |
| `status` | VARCHAR(16) | DEFAULT `'Active'` | Employment status (Active or Inactive) |

---

## Leave Requests Table

Stores all employee leave applications and approval information.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the leave request |
| `employee_id` | INTEGER | FOREIGN KEY (`employees.id`), NOT NULL | Employee submitting the leave request |
| `leave_type` | VARCHAR(32) | NOT NULL | Type of leave (Annual, Sick, Unpaid, etc.) |
| `start_date` | DATE | NOT NULL | Leave start date |
| `end_date` | DATE | NOT NULL | Leave end date |
| `status` | VARCHAR(16) | DEFAULT `'Pending'` | Request status (Pending, Approved, Rejected) |
| `reason` | TEXT | - | Reason provided by the employee |
| `approved_by` | INTEGER | FOREIGN KEY (`employees.id`) | Manager responsible for approval |
| `created_at` | DATETIME | DEFAULT `UTC_NOW` | Date and time the request was submitted |

---

## Payroll Records Table

Stores payroll information generated for each employee during a specific payroll period.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the payroll record |
| `employee_id` | INTEGER | FOREIGN KEY (`employees.id`), NOT NULL | Employee for whom payroll is generated |
| `period_start` | DATE | NOT NULL | Start date of the payroll period |
| `period_end` | DATE | NOT NULL | End date of the payroll period |
| `gross_pay` | NUMERIC(12,2) | NOT NULL | Employee's gross salary before deductions |
| `tax_deduction` | NUMERIC(12,2) | NOT NULL | Total tax deducted |
| `social_security_deduction` | NUMERIC(12,2) | NOT NULL | Social security contribution deducted |
| `unpaid_leave_deduction` | NUMERIC(12,2) | NOT NULL | Deduction resulting from approved unpaid leave |
| `net_pay` | NUMERIC(12,2) | NOT NULL | Final salary after all deductions |
| `status` | VARCHAR(16) | DEFAULT `'Draft'` | Payroll status (`Draft`, `Finalized`) |
| `generated_at` | DATETIME | DEFAULT `UTC_NOW` | Date and time the payroll record was generated |

---

# Business Logic

The application implements business rules that closely reflect real-world Human Resource and Payroll workflows instead of relying solely on basic CRUD operations.

---

## Leave Management Rules

The Leave Management module enforces several validation rules to ensure fairness, maintain operational continuity, and integrate seamlessly with payroll processing.

| Rule | Description |
|------|-------------|
| **Minimum Notice Period** | Annual leave requests must be submitted at least **7 days** before the requested start date to reduce last-minute disruptions. |
| **Team Coverage Validation** | No more than **50%** of active employees within the same team may have overlapping approved leave to prevent understaffing. |
| **Leave Overlap Prevention** | Employees cannot submit leave requests that overlap with existing approved or pending leave requests. |
| **Payroll Integration** | Approved unpaid leave is automatically considered during payroll generation, reducing the employee's gross salary proportionally. |

---

## Payroll Formula

Payroll calculations are performed automatically for each payroll period while considering employee start dates, unpaid leave, and statutory deductions.

### 1. Gross Pay

The employee's monthly salary serves as the base gross pay.

For employees who join during the payroll period, salary is automatically prorated based on the number of days worked.

**Formula**

```text
Daily Rate = Monthly Salary ÷ Total Days in Month

Gross Pay = Daily Rate × Days Worked
```

---

### 2. Unpaid Leave Deduction

Approved unpaid leave reduces the employee's gross salary.

**Formula**

```text
Unpaid Leave Deduction = Daily Rate × Number of Unpaid Leave Days
```

---

### 3. Social Security Deduction

A fixed social security contribution of **5%** is deducted from the employee's gross salary.

**Formula**

```text
Social Security = Gross Pay × 5%
```

---

### 4. Tax Calculation

A simplified progressive tax system is applied after calculating the taxable income.

| Taxable Income | Tax Rate |
|---------------|----------|
| Up to **$2,000** | 0% |
| **$2,001 – $5,000** | 10% of the amount above $2,000 |
| Above **$5,000** | 20% of the amount above $5,000, plus the tax from the previous bracket |

---

### 5. Net Pay

The employee's final salary is calculated after deducting social security, tax, and unpaid leave deductions.

**Formula**

```text
Net Pay =
Gross Pay
− Social Security Deduction
− Tax Deduction
− Unpaid Leave Deduction
```

---

# Frontend Overview

The frontend is developed using **HTML5**, **Tailwind CSS**, and **Vanilla JavaScript** to deliver a responsive and user-friendly interface that closely follows the provided Figma design.

The application is organized into multiple pages, each focusing on a specific HR function.

| Page | Description |
|------|-------------|
| **Dashboard** | Displays key HR metrics including total employees, employees currently on leave, pending leave approvals, monthly payroll summary, average salary, and visual charts for payroll and team distribution. |
| **Employees** | Lists all employees, supports adding and editing employee records, and provides a simple organizational hierarchy showing reporting relationships. |
| **Teams** | Displays all organizational teams and allows administrators to create and manage teams. |
| **Leave Management** | Enables employees to submit leave requests while allowing managers to approve or reject pending requests. The page also displays leave balances and company leave policies. |
| **Payroll** | Allows payroll administrators to generate monthly payroll, review payroll history, and view detailed employee payslips before finalization. |

---

# How to Run Locally

## Prerequisites

Before running the application, ensure the following software is installed:

| Requirement | Version |
|-------------|---------|
| Python | 3.8 or later |
| PostgreSQL | Latest Stable Version |
| pip | Latest Version |

---

## 1. Clone the Repository

```bash
git clone https://github.com/ombati003/hr-payroll-system

cd hr-payroll-system
```

---

## 2. Create and Activate a Virtual Environment

Creating a virtual environment keeps project dependencies isolated.

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```powershell
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Project Dependencies

```bash
pip install -r requirements/base.txt
```

---

## 4. Configure the Database

# Database Setup (PostgreSQL)

This project uses **PostgreSQL** as the primary database.

## Prerequisites

Ensure you have the following installed:

- PostgreSQL 14 or later
- Python 3.11+
- Git

## Clone the Repository

```bash
git clone https://github.com/ombati003/hr-payroll-system.git
cd hr-payroll-system
```

### Create the PostgreSQL Database

```sql
CREATE DATABASE hr_payroll;
```

---

### Configure Environment Variables

In a production environment, create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/hr_payroll

SECRET_KEY=your_super_secret_key
```

Replace `your_username` and `your_password` with your PostgreSQL credentials.

---

## Restore the Database

The repository contains a PostgreSQL SQL dump named:

```
hr_payroll_db.sql
```

Restore the database using:

```bash
psql -U postgres -d hr_payroll -f hr_payroll_db.sql
```

Alternatively:

```bash
psql -U postgres hr_payroll < hr_payroll_db.sql
```

If prompted, enter your PostgreSQL password.

## Configure Environment Variables
### Apply Database Migrations

Initialize and apply all database migrations.

```bash
flask db init

flask db migrate -m "Initial migration"

flask db upgrade
```

---

## 5. Run the Application

Start the Flask development server.

```bash
python run.py
```

After the server starts, open your browser and navigate to:

```text
http://127.0.0.1:5000/
```

---

# Testing

The project includes automated unit tests that validate the application's core business logic.

The tests focus on:

| Test Area | Description |
|-----------|-------------|
| Payroll Calculations | Verifies gross pay, deductions, and net pay calculations. |
| Leave Validation | Ensures leave requests follow business rules and validation requirements. |
| Team Coverage | Confirms staffing thresholds are respected during leave approval. |
| Tax Calculations | Validates all tax bracket calculations. |
| Payroll Generation | Ensures payroll records and payslips are generated correctly. |

Run the complete test suite using:

```bash
pytest
```

---

# Future Improvements

The following enhancements are planned for future versions of the system.

| Enhancement | Description |
|-------------|-------------|
| **Authentication & Authorization** | Implement Flask-Login with Role-Based Access Control (RBAC) for administrators, managers, and employees. |
| **Advanced Reporting** | Generate payroll analytics, leave trends, and departmental reports with downloadable exports. |
| **Notifications** | Add email and in-app notifications for leave approvals, payroll generation, and important HR events. |
| **Interactive Dashboard** | Integrate Chart.js to provide dynamic payroll, employee, and leave analytics. |
| **Employee Self-Service Portal** | Allow employees to view payslips, monitor leave balances, and update personal information. |
| **Administration Panel** | Provide a centralized interface for managing users, tax settings, leave policies, and company configuration. |
| **API Documentation** | Generate OpenAPI (Swagger) documentation for all REST API endpoints. |
| **Docker Support** | Containerize the application using Docker and Docker Compose for simplified deployment and consistent development environments. |

---

# License

This project was developed as part of a technical assessment to demonstrate practical software engineering skills in **Human Resource Management**, **Payroll Processing**, **Business Rule Implementation**, and **Full-Stack Web Development** using **Flask**, **PostgreSQL**, and **modern frontend technologies**.