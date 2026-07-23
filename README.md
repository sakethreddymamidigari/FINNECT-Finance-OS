# FINNECT Finance OS

> **A production-ready Loan Management System backend built with FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication for finance businesses.**

FINNECT Finance OS is a backend application designed to digitize the day-to-day operations of finance businesses. It manages the complete loan lifecycle—from customer onboarding and loan issuance to payment collection, renewals, settlements, and business reporting.

Unlike a basic CRUD application, FINNECT implements real-world financial business rules such as multiple interest calculation methods, interest-first payment allocation, loan renewals, settlement handling, and business dashboards.

---

## Key Features

### Authentication

* Finance Owner Registration
* Secure Login
* JWT Authentication
* Password Hashing using BCrypt
* Protected APIs

---

### Customer Management

* Register Customers
* Update Customer Information
* View Customer Details
* Search Customers
* List All Customers

---

### Loan Management

* Create Loans
* Update Loan Details
* View Loan Information
* Generate Loan Statements
* Dynamic Interest Summary
* Settlement Preview
* Loan Settlement
* Loan Renewal

---

### Payment Management

* Record Loan Payments
* Automatic Interest-First Allocation
* Principal Payment Tracking
* Latest Payment Deletion Validation
* Complete Payment History

---

### Interest Calculation

FINNECT supports two interest calculation methods commonly used by finance businesses.

#### Percentage Method

Monthly interest is calculated using a percentage of the outstanding principal.

Example:

* Principal: ₹100,000
* Interest Rate: 2% per month

---

#### Rupees per ₹100 Method

A traditional finance method where interest is charged as a fixed amount for every ₹100 borrowed.

Example:

* ₹3 per ₹100 per month

---

### Loan Renewal

Supports extension of active loans while maintaining renewal history.

* Updated Due Date
* Updated Interest Rate
* Updated Interest Method
* Renewal Notes
* Renewal History

---

### Loan Settlement

Allows early settlement of active loans.

Features include:

* Settlement Preview
* Interest-First Settlement
* Principal Adjustment
* Waived Amount Calculation
* Settlement Amount
* Settlement Reason
* Closure Type

---

### Dashboard & Reports

The dashboard provides business insights through dedicated reporting endpoints.

#### Dashboard Summary

* Total Customers
* Active Loans
* Closed Loans
* Total Principal Disbursed
* Remaining Principal
* Total Principal Paid
* Total Interest Paid
* Today's Collection
* Recent Loans
* Recent Payments

#### Business Reports

* Profit Summary
* Maturity Report
* Overdue Loans
* Closed Loans

---

# Tech Stack

| Category           | Technology       |
| ------------------ | ---------------- |
| Language           | Python           |
| Framework          | FastAPI          |
| Database           | PostgreSQL       |
| ORM                | SQLAlchemy       |
| Data Validation    | Pydantic         |
| Authentication     | JWT              |
| Password Hashing   | Passlib + BCrypt |
| Database Migration | Alembic          |
| API Documentation  | Swagger UI       |

---

# Project Architecture

```
Finance Owner
       │
       ▼
   Authentication
       │
       ▼
    Customers
       │
       ▼
      Loans
       │
 ┌─────┴───────────────┐
 ▼                     ▼
Payments          Loan Renewals
       │
       ▼
Loan Settlement
       │
       ▼
 Dashboard & Reports
```

---

# Project Structure

```
FINNECT-Finance-OS/

├── alembic/
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── database/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       ├── utils/
│       └── main.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

# Business Workflow

```
Finance Owner Login
          │
          ▼
Register Customer
          │
          ▼
Create Loan
          │
          ▼
Collect Payments
          │
     ┌────┴────┐
     ▼         ▼
Loan Renewal  Settlement
          │
          ▼
Dashboard Reports
```

---

# API Modules

## Authentication

```
POST /finance-owners/register
POST /finance-owners/login
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
PUT    /loans/{id}
GET    /loans/{id}

GET    /loans/{id}/statement
GET    /loans/{id}/interest-summary

GET    /loans/{id}/settlement-preview
POST   /loans/{id}/settlement

POST   /loans/{id}/renew
```

> Update this section if your API exposes additional loan endpoints.

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

# Running the Project

## Clone Repository

```bash
git clone https://github.com/sakethreddymamidigari/FINNECT-Finance-OS.git
cd FINNECT-Finance-OS
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file using `.env.example`.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/finnect
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start the Server

```bash
python -m uvicorn backend.app.main:app --reload
```

---

# API Documentation

Once the server is running:

```
http://127.0.0.1:8000/docs
```

Swagger UI provides interactive API documentation for every endpoint.

---

# Security

* JWT Authentication
* Password Hashing
* Protected Routes
* Request Validation using Pydantic
* SQLAlchemy ORM
* Secure Password Storage

---

# Future Enhancements

* WhatsApp Payment Reminders
* PDF Loan Statements
* Excel Report Export
* Dashboard Analytics & Charts
* Mobile Application
* Notification System

---

# Version

**Current Version:** **v1.0.0**

---

## Contributing

This repository currently serves as a personal portfolio project. Suggestions and improvements are welcome through issues or pull requests