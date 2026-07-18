# FINNECT Finance OS

FINNECT Finance OS is a scalable full-stack loan management platform designed for local finance businesses to replace traditional paper-based loan records with a secure, modern, and production-ready digital system.

The platform enables finance owners to manage customers, loans, repayments, and financial records while providing a scalable backend architecture that can later power web and mobile applications.

---

# Features

## Authentication

- Finance Owner Registration
- Secure Login
- JWT Authentication
- Password Hashing (bcrypt)
- Protected API Endpoints

---

## Customer Management

- Register Customers
- View Customer Details
- Customer Listing
- Customer–Finance Owner Association
- Multi-tenant Data Isolation

---

## Loan Management

- Create Loans
- Loan Status Tracking
- Customer–Loan Association
- Finance Owner–Loan Association
- Dynamic Interest Rate per Loan
- Multiple Interest Calculation Methods
    - Monthly Percentage
    - ₹ per ₹100 per Month
- Remaining Principal Tracking
- Total Principal Paid Tracking
- Total Interest Paid Tracking
- Interest Calculation Timeline

---

## Payment Infrastructure

- Payment Database Design
- Payment History Tracking
- Loan–Payment Relationship
- Finance Owner–Payment Relationship
- Production-ready Payment Schema

---

# Roadmap

## Payment Module

- Payment APIs
- Interest Calculation Engine
- Automatic Interest Allocation
- Automatic Principal Allocation
- Loan Closure Logic

## Dashboard

- Total Customers
- Active Loans
- Closed Loans
- Outstanding Amount
- Monthly Collections
- Interest Earned
- Profit Summary

## Reports

- Customer Statements
- Loan Statements
- Payment Statements
- Profit Reports
- Collection Reports

## Search & Filters

- Customer Search
- Mobile Number Search
- Loan Status Filter
- Due Date Filter
- Date Range Reports

## Security

- Role-based Authorization
- Global Exception Handling
- Request Validation
- Secure API Responses

## Deployment

- Docker
- Production Configuration
- Cloud Deployment

---

# Future Enhancements

- WhatsApp payment and loan maturity reminders
- AI voice calling agents for automated customer reminders
- Mobile application
- OCR-based paper loan digitization
- AI-powered financial insights
- Multi-language support

---

# Tech Stack

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic
- Pydantic

### Authentication

- JWT
- Passlib (bcrypt)

### Documentation

- Swagger UI
- OpenAPI

### DevOps

- Docker (Planned)
- Git
- GitHub

---

# Project Structure

```text
FINNECT/
│
├── alembic/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── README.md
│
└── .env
```

---

# Architecture

FINNECT follows a layered architecture to improve maintainability, scalability, and testability.

```
Client
   │
REST API
   │
API Layer
   │
Service Layer
   │
Database Layer
   │
PostgreSQL
```

Database schema changes are managed using Alembic migrations to ensure safe and version-controlled schema evolution.

---

# Database Design

Core entities:

- Finance Owners
- Customers
- Loans
- Payments

Relationships:

- One Finance Owner → Many Customers
- One Finance Owner → Many Loans
- One Finance Owner → Many Payments
- One Customer → Many Loans
- One Loan → Many Payments

---

# Current Status

**Version:** v0.5.0

## Completed

- Authentication Module
- Customer Management Module
- Loan Management Module
- Payment Database Infrastructure
- Alembic Migration System
- Production-ready Database Schema

## Currently Developing

- Payment Service
- Interest Calculation Engine
- Payment APIs

---

# Vision

FINNECT aims to become a comprehensive Finance Management Operating System that enables local finance businesses to digitally manage lending operations, automate financial calculations, improve operational efficiency, and scale seamlessly from small finance offices to enterprise-level lending platforms.

---

# License

This project is under active development.