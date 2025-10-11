import bcrypt
from .db import engine, Base, SessionLocal
# Import all models here to ensure they are registered with the Base metadata
from . import models

def init_database():
    """
    Initializes the database by creating tables and seeding initial data.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if demo user exists
        demo_user = db.query(models.User).filter(models.User.email == "demo@portfolio.com").first()
        if not demo_user:
            # Hash the password
            hashed_password = bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt())

            # Create demo user
            new_user = models.User(
                email="demo@portfolio.com",
                password=hashed_password.decode('utf-8'),
                name="Demo User"
            )
            db.add(new_user)
            print("Demo user created.")

        # Check if ETF master data exists
        etf_count = db.query(models.ETFMaster).count()
        if etf_count == 0:
            sample_etfs = [
                models.ETFMaster(symbol="NIFTYBEES", full_name="Nippon India ETF Nifty 50 BeES", amc="Nippon India", underlying_index="Nifty 50", isin="INF204K01131"),
                models.ETFMaster(symbol="JUNIORBEES", full_name="Nippon India ETF Nifty Next 50 Junior BeES", amc="Nippon India", underlying_index="Nifty Next 50", isin="INF204K01149"),
                models.ETFMaster(symbol="BANKBEES", full_name="Nippon India ETF Nifty Bank BeES", amc="Nippon India", underlying_index="Nifty Bank", isin="INF204K01040"),
                models.ETFMaster(symbol="LIQUIDBEES", full_name="Nippon India ETF Liquid BeES", amc="Nippon India", underlying_index="CRISIL Liquid Debt Index", isin="INF732E01037"),
                models.ETFMaster(symbol="GOLDBEES", full_name="Nippon India ETF Gold BeES", amc="Nippon India", underlying_index="Price of Gold", isin="INF204K01073"),
            ]
            db.bulk_save_objects(sample_etfs)
            print("Sample ETFs seeded.")

        db.commit()
        print("Database initialized successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    init_database()