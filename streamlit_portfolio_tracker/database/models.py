from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    Time,
    Boolean,
    ForeignKey,
    DECIMAL,
    TIMESTAMP,
    TEXT,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .db import Base

class TransactionType(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"
    SIP = "SIP"
    DIVIDEND = "DIVIDEND"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255))
    currency = Column(String(3), default="INR")
    currency_symbol = Column(String(5), default="₹")
    sip_day = Column(Integer, default=5)
    sip_amount = Column(DECIMAL(12, 2), default=15000)
    enable_email_alerts = Column(Boolean, default=True)
    enable_auto_sip = Column(Boolean, default=False)
    pe_update_frequency = Column(String(20), default="DAILY")
    rebalance_threshold = Column(DECIMAL(5, 2), default=25.00)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    portfolios = relationship("Portfolio", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    pe_matrix_entries = relationship("PEMatrix", back_populates="user")
    snapshots = relationship("Snapshot", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class ETFMaster(Base):
    __tablename__ = "etf_master"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    amc = Column(String(100))
    underlying_index = Column(String(100))
    category = Column(String(50))
    expense_ratio = Column(DECIMAL(5, 2))
    aum = Column(DECIMAL(15, 2))
    launch_date = Column(Date)
    isin = Column(String(20), unique=True, index=True)
    trading_symbol = Column(String(50))
    lot_size = Column(Integer, default=1)
    tracking_error = Column(DECIMAL(5, 2))
    current_price = Column(DECIMAL(12, 2))
    last_updated = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())

    portfolios = relationship("Portfolio", back_populates="etf")
    transactions = relationship("Transaction", back_populates="etf")
    pe_matrix_entries = relationship("PEMatrix", back_populates="etf")
    snapshot_details = relationship("SnapshotDetail", back_populates="etf")
    alerts = relationship("Alert", back_populates="etf")

class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    etf_id = Column(Integer, ForeignKey("etf_master.id", ondelete="RESTRICT"), nullable=False, index=True)
    units_held = Column(DECIMAL(15, 4), nullable=False)
    avg_buy_price = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="portfolios")
    etf = relationship("ETFMaster", back_populates="portfolios")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    etf_id = Column(Integer, ForeignKey("etf_master.id", ondelete="RESTRICT"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time)
    type = Column(SQLAlchemyEnum(TransactionType), nullable=False, index=True)
    units = Column(DECIMAL(15, 4), nullable=False)
    price_per_unit = Column(DECIMAL(12, 2), nullable=False)
    total_amount = Column(DECIMAL(15, 2))
    brokerage = Column(DECIMAL(10, 2), default=0)
    stt = Column(DECIMAL(10, 2), default=0)
    gst = Column(DECIMAL(10, 2), default=0)
    net_amount = Column(DECIMAL(15, 2))
    broker = Column(String(50))
    order_id = Column(String(100))
    remarks = Column(TEXT)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship("User", back_populates="transactions")
    etf = relationship("ETFMaster", back_populates="transactions")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_name = Column(String(200), nullable=False)
    target_amount = Column(DECIMAL(15, 2), nullable=False)
    target_date = Column(Date, nullable=False)
    current_allocation = Column(DECIMAL(15, 2), default=0)
    monthly_sip = Column(DECIMAL(12, 2), default=0)
    expected_return = Column(DECIMAL(5, 2))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship("User", back_populates="goals")

class PEMatrix(Base):
    __tablename__ = "pe_matrix"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    etf_id = Column(Integer, ForeignKey("etf_master.id", ondelete="RESTRICT"), nullable=False)
    current_pe = Column(DECIMAL(8, 2), nullable=False)
    avg_pe_3y = Column(DECIMAL(8, 2), nullable=False)
    avg_pe_5y = Column(DECIMAL(8, 2), nullable=False)
    last_updated = Column(TIMESTAMP, default=func.now())

    user = relationship("User", back_populates="pe_matrix_entries")
    etf = relationship("ETFMaster", back_populates="pe_matrix_entries")

class Snapshot(Base):
    __tablename__ = "snapshots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False)
    total_invested = Column(DECIMAL(15, 2), nullable=False)
    current_value = Column(DECIMAL(15, 2), nullable=False)
    unrealized_gain = Column(DECIMAL(15, 2))
    gain_percent = Column(DECIMAL(8, 2))
    xirr = Column(DECIMAL(8, 2))
    benchmark_return = Column(DECIMAL(8, 2))
    alpha = Column(DECIMAL(8, 2))
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship("User", back_populates="snapshots")
    details = relationship("SnapshotDetail", back_populates="snapshot")

class SnapshotDetail(Base):
    __tablename__ = "snapshot_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_id = Column(Integer, ForeignKey("snapshots.id", ondelete="CASCADE"), nullable=False)
    etf_id = Column(Integer, ForeignKey("etf_master.id", ondelete="RESTRICT"), nullable=False)
    value = Column(DECIMAL(15, 2), nullable=False)
    units = Column(DECIMAL(15, 4), nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)

    snapshot = relationship("Snapshot", back_populates="details")
    etf = relationship("ETFMaster", back_populates="snapshot_details")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    etf_id = Column(Integer, ForeignKey("etf_master.id", ondelete="CASCADE"), nullable=True)
    alert_type = Column(String(50), nullable=False)
    condition = Column(String(50), nullable=False)
    threshold = Column(DECIMAL(10, 2), nullable=False)
    triggered = Column(Boolean, default=False)
    last_triggered = Column(TIMESTAMP)
    notification_method = Column(String(20), default="EMAIL")
    email_sent = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())

    user = relationship("User", back_populates="alerts")
    etf = relationship("ETFMaster", back_populates="alerts")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    timestamp = Column(TIMESTAMP, default=func.now())
    action = Column(String(50))
    model_name = Column(String(100))
    object_id = Column(String(100))
    field_name = Column(String(100))
    old_value = Column(TEXT)
    new_value = Column(TEXT)
    ip_address = Column(String(45))
    user_agent = Column(TEXT)

    user = relationship("User", back_populates="audit_logs")