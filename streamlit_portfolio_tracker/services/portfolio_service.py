from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import Portfolio, ETFMaster, Transaction, Snapshot, SnapshotDetail, User
from sqlalchemy import func, desc
import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_portfolio_summary(user_id: int):
    """
    Calculates a summary of the user's portfolio.
    """
    db: Session = next(get_db())

    holdings = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    total_invested = 0
    current_value = 0

    if not holdings:
        return {
            "total_invested": 0,
            "current_value": 0,
            "total_gain": 0,
            "gain_percent": 0,
            "total_etfs": 0,
            "best_performer": {"symbol": "-", "gain_percent": 0},
            "worst_performer": {"symbol": "-", "gain_percent": 0},
        }

    for holding in holdings:
        etf = holding.etf
        invested = holding.units_held * holding.avg_buy_price
        # Use a placeholder for live price if not available
        current_price = etf.current_price if etf.current_price else holding.avg_buy_price
        value = holding.units_held * current_price

        total_invested += invested
        current_value += value

    total_gain = current_value - total_invested
    gain_percent = (total_gain / total_invested * 100) if total_invested > 0 else 0

    # Best/worst performers can be added here later

    return {
        "total_invested": total_invested,
        "current_value": current_value,
        "total_gain": total_gain,
        "gain_percent": gain_percent,
        "total_etfs": len(holdings),
        "best_performer": {"symbol": "TBD", "gain_percent": 0},
        "worst_performer": {"symbol": "TBD", "gain_percent": 0},
    }

def get_full_portfolio(user_id: int):
    """
    Retrieves the full portfolio details for a user.
    """
    db: Session = next(get_db())

    holdings = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    portfolio_list = []
    total_portfolio_value = 0

    # First pass to calculate total value
    for holding in holdings:
        current_price = holding.etf.current_price if holding.etf.current_price else holding.avg_buy_price
        total_portfolio_value += holding.units_held * current_price

    if total_portfolio_value == 0:
        return []

    for holding in holdings:
        etf = holding.etf
        invested = holding.units_held * holding.avg_buy_price
        current_price = etf.current_price if etf.current_price else holding.avg_buy_price
        current_val = holding.units_held * current_price
        gain_loss = current_val - invested
        gain_percent = (gain_loss / invested * 100) if invested > 0 else 0
        allocation = (current_val / total_portfolio_value * 100) if total_portfolio_value > 0 else 0

        status = "Positive"
        if gain_percent > 10: status = "Strong"
        if gain_percent < 0: status = "Loss"

        portfolio_list.append({
            "symbol": etf.symbol,
            "full_name": etf.full_name,
            "units_held": holding.units_held,
            "avg_buy_price": holding.avg_buy_price,
            "current_price": current_price,
            "total_invested": invested,
            "current_value": current_val,
            "unrealized_gain": gain_loss,
            "gain_percent": gain_percent,
            "allocation": allocation,
            "status": status,
            "etf_id": etf.id
        })

    return portfolio_list

def get_portfolio_allocation(user_id: int):
    """
    Gets the portfolio allocation for pie chart visualization.
    """
    portfolio = get_full_portfolio(user_id)
    return [{"symbol": item["symbol"], "value": item["current_value"]} for item in portfolio]

def update_portfolio_from_transactions(user_id: int):
    """
    Recalculates portfolio holdings based on all transactions for a user.
    This is a complex FIFO implementation and will be simplified for now.
    """
    # This is a key function but complex.
    # A simplified version will be implemented first.
    # For now, let's assume a simple aggregation.
    db: Session = next(get_db())

    # Delete existing portfolio to recalculate
    db.query(Portfolio).filter(Portfolio.user_id == user_id).delete()

    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.date).all()

    holdings = {} # etf_id -> {units, invested_amount}

    for t in transactions:
        if t.etf_id not in holdings:
            holdings[t.etf_id] = {"units": 0, "invested": 0}

        if t.type in ["BUY", "SIP"]:
            holdings[t.etf_id]["units"] += t.units
            holdings[t.etf_id]["invested"] += t.units * t.price_per_unit
        elif t.type == "SELL":
            # Simple reduction for now, not FIFO
            avg_price = holdings[t.etf_id]["invested"] / holdings[t.etf_id]["units"] if holdings[t.etf_id]["units"] > 0 else 0
            holdings[t.etf_id]["invested"] -= t.units * avg_price
            holdings[t.etf_id]["units"] -= t.units

    for etf_id, data in holdings.items():
        if data["units"] > 0.0001: # Threshold to avoid floating point issues
            avg_buy_price = data["invested"] / data["units"]
            new_holding = Portfolio(
                user_id=user_id,
                etf_id=etf_id,
                units_held=data["units"],
                avg_buy_price=avg_buy_price
            )
            db.add(new_holding)

    db.commit()
    return True

def create_snapshot(user_id: int):
    """
    Creates a daily snapshot of the user's portfolio.
    """
    db: Session = next(get_db())

    # Check if snapshot for today already exists
    today = datetime.date.today()
    if db.query(Snapshot).filter(Snapshot.user_id == user_id, Snapshot.date == today).first():
        return False, "Snapshot for today already exists."

    summary = get_portfolio_summary(user_id)

    new_snapshot = Snapshot(
        user_id=user_id,
        date=today,
        total_invested=summary["total_invested"],
        current_value=summary["current_value"],
        unrealized_gain=summary["total_gain"],
        gain_percent=summary["gain_percent"]
    )
    db.add(new_snapshot)
    db.flush() # To get the snapshot ID

    full_portfolio = get_full_portfolio(user_id)
    for holding in full_portfolio:
        detail = SnapshotDetail(
            snapshot_id=new_snapshot.id,
            etf_id=holding["etf_id"],
            value=holding["current_value"],
            units=holding["units_held"],
            price=holding["current_price"]
        )
        db.add(detail)

    db.commit()
    return True, "Snapshot created successfully."

def get_recent_transactions(user_id: int, limit: int = 5):
    """
    Fetches the most recent transactions for the user.
    """
    db: Session = next(get_db())

    transactions = db.query(Transaction).join(ETFMaster).filter(Transaction.user_id == user_id).order_by(desc(Transaction.date)).limit(limit).all()

    return [
        {
            "date": t.date,
            "symbol": t.etf.symbol,
            "type": t.type.value,
            "units": t.units,
            "price": t.price_per_unit,
            "net_amount": t.net_amount
        } for t in transactions
    ]

def get_performance_history(user_id: int):
    """
    Retrieves historical performance data from snapshots.
    """
    db: Session = next(get_db())

    history = db.query(Snapshot).filter(Snapshot.user_id == user_id).order_by(Snapshot.date).all()

    return [
        {
            "date": s.date,
            "invested": s.total_invested,
            "current_value": s.current_value,
            "gain": s.unrealized_gain
        } for s in history
    ]

def delete_holding(user_id: int, etf_id: int):
    """
    Deletes a holding from the portfolio.
    NOTE: This is a destructive action and should be used with caution.
    It's often better to archive or mark as inactive.
    """
    db: Session = next(get_db())

    holding = db.query(Portfolio).filter(Portfolio.user_id == user_id, Portfolio.etf_id == etf_id).first()

    if holding:
        db.delete(holding)
        # Also delete associated transactions? For now, no.
        db.commit()
        return True
    return False