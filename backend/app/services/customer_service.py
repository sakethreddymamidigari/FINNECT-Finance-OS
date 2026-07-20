from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.app.models.customer import Customer
from backend.app.schemas.customer import CustomerCreate


def create_customer(
    db: Session,
    customer: CustomerCreate,
    finance_owner_id: int,
) -> Customer:
    """
    Create a new customer for the authenticated finance owner.
    """

    db_customer = Customer(
        full_name=customer.full_name,
        phone=customer.phone,
        address=customer.address,
        finance_owner_id=finance_owner_id,
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_customers(
    db: Session,
    finance_owner_id: int,
):
    """
    Return all customers belonging to the authenticated finance owner.
    """

    return (
        db.query(Customer)
        .filter(Customer.finance_owner_id == finance_owner_id)
        .all()
    )


def get_customer_names(
    db: Session,
    finance_owner_id: int,
):
    """
    Return only customer IDs and names for dropdown selection.
    """

    return (
        db.query(Customer.id, Customer.full_name)
        .filter(Customer.finance_owner_id == finance_owner_id)
        .order_by(Customer.full_name)
        .all()
    )

def search_customers(
    db: Session,
    finance_owner_id: int,
    query: str,
):
    """
    Search customers by name or phone.
    """

    return (
        db.query(Customer)
        .filter(
            Customer.finance_owner_id == finance_owner_id,
            or_(
                Customer.full_name.ilike(f"%{query}%"),
                Customer.phone.ilike(f"%{query}%"),
            ),
        )
        .order_by(Customer.full_name)
        .all()
    )