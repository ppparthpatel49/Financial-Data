from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import Transaction, TransactionType
from services.portfolio_service import update_portfolio_from_transactions
import pandas as pd
from decimal import Decimal
import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_transactions(user_id: int, filters: dict = None):
    """
    Fetches transactions for a user with optional filters.
    """
    db: Session = next(get_db())
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if filters:
        if filters.get("etf_id"):
            query = query.filter(Transaction.etf_id == filters["etf_id"])
        if filters.get("type"):
            query = query.filter(Transaction.type == TransactionType[filters["type"]])
        if filters.get("start_date"):
            query = query.filter(Transaction.date >= filters["start_date"])
        if filters.get("end_date"):
            query = query.filter(Transaction.date <= filters["end_date"])

    return query.order_by(Transaction.date.desc()).all()

def add_transaction(user_id: int, data: dict):
    """
    Adds a new transaction and updates the portfolio.
    """
    db: Session = next(get_db())

    try:
        # Calculate derived values
        units = Decimal(data['units'])
        price_per_unit = Decimal(data['price_per_unit'])
        brokerage = Decimal(data.get('brokerage', 0))

        total_amount = units * price_per_unit
        stt = total_amount * Decimal('0.001')  # 0.1%
        gst = brokerage * Decimal('0.18')  # 18%

        if data['type'] == 'SELL':
            net_amount = total_amount - (brokerage + stt + gst)
        else: # BUY, SIP
            net_amount = total_amount + brokerage + stt + gst


        new_transaction = Transaction(
            user_id=user_id,
            etf_id=data['etf_id'],
            date=data['date'],
            time=data.get('time'),
            type=TransactionType[data['type']],
            units=units,
            price_per_unit=price_per_unit,
            brokerage=brokerage,
            broker=data.get('broker'),
            order_id=data.get('order_id'),
            remarks=data.get('remarks'),
            total_amount=total_amount,
            stt=stt,
            gst=gst,
            net_amount=net_amount
        )

        db.add(new_transaction)
        db.commit()

        # After adding transaction, update the portfolio
        update_portfolio_from_transactions(user_id)

        return True, "Transaction added successfully."
    except Exception as e:
        db.rollback()
        return False, f"Failed to add transaction: {e}"
    finally:
        db.close()

def import_transactions_from_csv(user_id: int, df: pd.DataFrame):
    """
    Bulk imports transactions from a pandas DataFrame.
    """
    db: Session = next(get_db())

    success_count = 0
    error_count = 0
    errors = []

    # Expected columns, can be made more robust
    required_columns = ['date', 'type', 'etf_symbol', 'units', 'price_per_unit']

    for index, row in df.iterrows():
        try:
            # Basic validation
            if not all(col in row for col in required_columns):
                raise ValueError(f"Missing required columns in row {index+1}")

            # Data conversion and preparation
            transaction_data = {
                'date': pd.to_datetime(row['date']).date(),
                'type': row['type'].upper(),
                'units': row['units'],
                'price_per_unit': row['price_per_unit'],
                'brokerage': row.get('brokerage', 0),
                'broker': row.get('broker'),
                'order_id': row.get('order_id'),
                'remarks': row.get('remarks')
            }

            # Find etf_id from symbol
            from database.models import ETFMaster
            etf = db.query(ETFMaster).filter(ETFMaster.symbol == row['etf_symbol']).first()
            if not etf:
                raise ValueError(f"ETF symbol '{row['etf_symbol']}' not found in database.")

            transaction_data['etf_id'] = etf.id

            success, msg = add_transaction(user_id, transaction_data)
            if success:
                success_count += 1
            else:
                raise Exception(msg)

        except Exception as e:
            error_count += 1
            errors.append(f"Row {index + 2}: {e}")

    # A single portfolio update after all successful imports might be more efficient
    # but the current add_transaction already does it. For bulk, this can be optimized.

    return {"success": success_count, "errors": error_count, "error_details": errors}