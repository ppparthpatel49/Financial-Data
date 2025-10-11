import streamlit as st
from services.transaction_service import get_transactions, add_transaction, import_transactions_from_csv
from database.db import SessionLocal
from database.models import ETFMaster
from utils.auth import check_authentication
import pandas as pd
import datetime

st.set_page_config(page_title="Transactions", layout="wide")

if not check_authentication():
    st.warning("Please log in to view this page.")
    st.stop()

st.title("💰 Transactions Management")

user_id = st.session_state.user['id']

# Fetch ETFs for dropdowns
@st.cache_data
def get_etf_options():
    db = SessionLocal()
    try:
        etfs = db.query(ETFMaster).all()
        return {etf.symbol: etf.id for etf in etfs}
    finally:
        db.close()

etf_options = get_etf_options()
etf_symbols = list(etf_options.keys())

tab1, tab2, tab3 = st.tabs(["View Transactions", "Add Transaction", "Import from CSV"])

# --- TAB 1: View Transactions ---
with tab1:
    st.header("Your Transaction History")

    # Filters
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    with filter_col1:
        selected_etf_symbol = st.selectbox("Filter by ETF", options=["All"] + etf_symbols, key="view_etf")
    with filter_col2:
        selected_type = st.selectbox("Filter by Type", options=["All", "BUY", "SELL", "SIP", "DIVIDEND"])
    with filter_col3:
        start_date = st.date_input("Start Date", value=None)
    with filter_col4:
        end_date = st.date_input("End Date", value=datetime.date.today())

    # Build filter dictionary
    filters = {}
    if selected_etf_symbol != "All":
        filters["etf_id"] = etf_options[selected_etf_symbol]
    if selected_type != "All":
        filters["type"] = selected_type
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date

    try:
        transactions = get_transactions(user_id, filters)
        if transactions:
            # Join with ETF data for display
            data_to_display = []
            for t in transactions:
                data_to_display.append({
                    "Date": t.date,
                    "ETF": t.etf.symbol,
                    "Type": t.type.value,
                    "Units": t.units,
                    "Price/Unit": t.price_per_unit,
                    "Net Amount": t.net_amount,
                    "Broker": t.broker
                })
            df = pd.DataFrame(data_to_display)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions found matching your criteria.")
    except Exception as e:
        st.error(f"Failed to load transactions: {e}")


# --- TAB 2: Add Transaction ---
with tab2:
    st.header("Add a New Transaction")
    with st.form("add_transaction_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Date", datetime.date.today())
            units = st.number_input("Units", min_value=0.0, format="%.4f")
            broker = st.text_input("Broker (e.g., Zerodha)")
        with col2:
            txn_type = st.selectbox("Transaction Type", options=["BUY", "SELL", "SIP"])
            price_per_unit = st.number_input("Price per Unit", min_value=0.0, format="%.2f")
            order_id = st.text_input("Order ID (optional)")
        with col3:
            etf_symbol = st.selectbox("Select ETF", options=etf_symbols, key="add_etf")
            brokerage = st.number_input("Brokerage", min_value=0.0, format="%.2f", value=0.0)
            remarks = st.text_area("Remarks (optional)")

        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            if not etf_symbol or units == 0 or price_per_unit == 0:
                st.warning("Please fill in all required fields (ETF, Units, Price).")
            else:
                transaction_data = {
                    "etf_id": etf_options[etf_symbol],
                    "date": date,
                    "type": txn_type,
                    "units": str(units),
                    "price_per_unit": str(price_per_unit),
                    "brokerage": str(brokerage),
                    "broker": broker,
                    "order_id": order_id,
                    "remarks": remarks,
                }
                success, message = add_transaction(user_id, transaction_data)
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)

# --- TAB 3: Import from CSV ---
with tab3:
    st.header("Import Transactions from CSV")
    st.info("""
        Upload a CSV file with the following columns:
        - **date** (YYYY-MM-DD)
        - **type** (BUY, SELL, or SIP)
        - **etf_symbol** (e.g., NIFTYBEES)
        - **units** (e.g., 10.5)
        - **price_per_unit** (e.g., 150.25)
        - Optional columns: `brokerage`, `broker`, `order_id`, `remarks`
    """)

    sample_data = {
        'date': ['2023-01-15', '2023-01-20'],
        'type': ['BUY', 'SELL'],
        'etf_symbol': ['NIFTYBEES', 'GOLDBEES'],
        'units': [100, 50],
        'price_per_unit': [200.50, 45.10],
        'brokerage': [10.0, 5.0]
    }
    sample_df = pd.DataFrame(sample_data)
    st.download_button(
        label="Download Sample CSV",
        data=sample_df.to_csv(index=False).encode('utf-8'),
        file_name='sample_transactions.csv',
        mime='text/csv',
    )

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of your data:")
            st.dataframe(df.head())

            if st.button("Import Data"):
                with st.spinner("Importing..."):
                    result = import_transactions_from_csv(user_id, df)
                    st.success(f"Successfully imported {result['success']} transactions.")
                    if result['errors'] > 0:
                        st.error(f"Failed to import {result['errors']} transactions.")
                        with st.expander("View Error Details"):
                            for error in result['error_details']:
                                st.write(error)
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")