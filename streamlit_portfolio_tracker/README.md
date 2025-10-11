# Streamlit Portfolio Tracker

This is a comprehensive portfolio tracking application built with Streamlit. It allows users to manage their ETF portfolios, track performance, analyze valuation, and get tax reports.

## Features

- **Dashboard:** At-a-glance view of your portfolio's key metrics.
- **Portfolio Management:** Detailed view of all your holdings.
- **Transaction Tracking:** Add, view, and import transactions.
- **Goal Setting:** Set and track financial goals.
- **P/E Valuation Matrix:** Analyze market valuation based on Price-to-Earnings ratios.
- **Drawdown Analysis:** Understand portfolio risk and volatility.
- **Tax Reporting:** Generate capital gains reports for tax filing.
- **Alerts:** Set up custom alerts for market movements and portfolio events.

## Installation & Setup

### Step 1: Environment Setup

```bash
# Clone or create project directory
mkdir streamlit_portfolio_tracker
cd streamlit_portfolio_tracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# For example, update your database URL or email API keys
nano .env
```

### Step 3: Database Initialization

```bash
# Create data directory
mkdir data

# Initialize database
python -c "from database.init_db import init_database; init_database()"

# This will:
# 1. Create all tables
# 2. Create a demo user (demo@portfolio.com / demo123)
# 3. Seed sample ETF data
```

### Step 4: Run Application

```bash
# Start Streamlit
streamlit run app.py

# The application will open at http://localhost:8501

# Login with:
# Email: demo@portfolio.com
# Password: demo123
```