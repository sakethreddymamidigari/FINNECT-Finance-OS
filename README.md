# FINNECT Finance OS

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge" />
  <img src="https://img.shields.io/badge/JWT-Authentication-black?style=for-the-badge" />
</p>

## Overview

FINNECT Finance OS is a backend system built for finance businesses to manage customers, loans, payments, renewals, settlements, and business insights from a single platform.

The application is designed around real-world lending workflows instead of basic CRUD operations. It supports multiple interest calculation methods, loan renewals, settlements, payment tracking, and dashboard reports.

---

# Features

## Authentication

- Finance Owner Registration
- Finance Owner Login
- JWT Authentication
- Password Hashing
- Protected APIs

---

## Customer Management

- Register Customer
- Update Customer
- View Customer
- Search Customers
- List Customers

---

## Loan Management

- Create Loan
- Update Loan
- View Loan Details
- Loan Statement
- Interest Summary
- Settlement Preview
- Loan Settlement
- Loan Renewal

---

## Payment Management

- Add Payment
- Interest-first payment allocation
- Principal payment handling
- Latest payment deletion restriction
- Payment history

---

## Interest Calculation

FINNECT supports two different interest calculation methods.

### Percentage Method

Monthly interest calculated using percentage.

Example

- Principal : ₹100000
- Interest : 2% per month

---

### Rupees Per ₹100 Method

Commonly used by local finance businesses.

Example

- ₹3 per ₹100 per month

---

## Loan Renewal

Supports extending active loans while preserving complete renewal history.

Features

- New Due Date
- New Interest Rate
- New Interest Method
- Renewal Notes
- Renewal Tracking

---

## Loan Settlement

Supports settlement of active loans.

Features

- Settlement Preview
- Interest First Settlement
- Principal Adjustment
- Waived Amount Calculation
- Settlement Amount
- Settlement Reason
- Closure Type

---

## Dashboard

Dashboard provides business insights.

### Summary

- Total Customers
- Active Loans
- Closed Loans
- Total Principal Disbursed
- Remaining Principal
- Total Principal Paid
- Total Interest Paid
- Today's Collection

### Reports

- Profit Summary
- Maturity Report
- Overdue Loans
- Closed Loans

---

# Technology Stack

| Category         | Technology       |
|------------------|------------------|
| Language         | Python           |
| Framework        | FastAPI          |
| ORM              | SQLAlchemy       |
| Database         | PostgreSQL       |
| Authentication   | JWT              |
| Password Hashing | Passlib + BCrypt |
| Validation       | Pydantic         |
| API Documentation| Swagger UI       |
| Migrations       | Alembic          |

---

# Project Structure

```
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── alembic/
│
├── requirements.txt
│
└── README.md
```

---

# Database Design

```
Finance Owner
      │
      ▼
 Customer
      │
      ▼
    Loan
      │
      ├──────────────┐
      ▼              ▼
 Payment        Loan Renewal
```

---

# Business Workflow

```
Finance Owner Login

        │

Create Customer

        │

Create Loan

        │

Receive Payments

        │

Renew Loan (Optional)

        │

Settlement (Optional)

        │

Dashboard Reports
```

---

# API Modules

## Authentication

```
POST   /finance-owners/register
POST   /finance-owners/login
```

---

## Customers

```
POST   /customers
GET    /customers
GET    /customers/{id}
PUT    /customers/{id}
GET    /customers/search
```

---

## Loans

```
POST   /loans
GET    /loans
GET    /loans/{id}
PUT    /loans/{id}

GET    /loans/{id}/statement
GET    /loans/{id}/interest-summary

GET    /loans/{id}/settlement-preview
POST   /loans/{id}/settlement

POST   /loans/{id}/renew
```

---

## Payments

```
POST   /payments
PUT    /payments/{id}
DELETE /payments/{id}
```

---

## Dashboard

```
GET /dashboard

GET /dashboard/profit-summary

GET /dashboard/maturity-report

GET /dashboard/overdue-loans

GET /dashboard/closed-loans
```

---

# API Documentation

After starting the server

```
http://127.0.0.1:8000/docs
```

Interactive Swagger UI

---

# Installation

Clone the repository

```bash
git clone https://github.com/sakethreddymamidigari/FINNECT-Finance-OS.git
```

Move into the project

```bash
cd FINNECT-Finance-OS
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
alembic upgrade head
```

Run the application

```bash
python -m uvicorn backend.app.main:app --reload
```

---

# Environment Variables

Create a `.env` file.

```
DATABASE_URL=postgresql://username:password@localhost:5432/finnect

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Security

- JWT Authentication
- Password Hashing
- Protected Routes
- Input Validation
- SQLAlchemy ORM
- Pydantic Validation

---

# Future Enhancements

- WhatsApp Payment Reminders
- Export Reports to Excel
- PDF Statements
- Notification System
- Dashboard Charts
- Analytics
- Mobile Application

---

# Version

Current Version

```
v1.0.0
``'