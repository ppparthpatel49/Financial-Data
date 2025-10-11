import streamlit as st
from services.portfolio_service import (
    get_portfolio_summary,
    get_portfolio_allocation,
    get_recent_transactions,
    get_performance_history,
    create_snapshot
)
from utils.auth import check_authentication
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

if not check_authentication():
    st.warning("Please log in to view this page.")
    st.stop()

st.title("📊 Dashboard")

# --- DATA LOADING ---
try:
    user_id = st.session_state.user['id']
    summary = get_portfolio_summary(user_id)
    allocation = get_portfolio_allocation(user_id)
    recent_txn = get_recent_transactions(user_id, limit=5)
    performance = get_performance_history(user_id)
except Exception as e:
    st.error(f"Failed to load dashboard data: {e}")
    st.stop()

# --- HEADER & KPIs ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Invested", f"₹{summary.get('total_invested', 0):,.2f}")
with col2:
    st.metric("Current Value", f"₹{summary.get('current_value', 0):,.2f}")
with col3:
    gain_value = summary.get('total_gain', 0)
    gain_percent = summary.get('gain_percent', 0)
    st.metric("Total Gain/Loss", f"₹{gain_value:,.2f}", delta=f"{gain_percent:.2f}%")
with col4:
    st.metric("Total ETFs", summary.get('total_etfs', 0))

st.markdown("---")

# --- CHARTS ---
if not allocation and not performance:
    st.info("Add transactions to see your dashboard charts and data.")
else:
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("Portfolio Allocation")
        if allocation:
            alloc_df = pd.DataFrame(allocation)
            fig_alloc = px.pie(alloc_df, names='symbol', values='value', title='Asset Allocation by Value')
            st.plotly_chart(fig_alloc, use_container_width=True)
        else:
            st.info("No holdings to display allocation.")

    with chart_col2:
        st.subheader("Portfolio Growth")
        if performance:
            perf_df = pd.DataFrame(performance)
            perf_df['date'] = pd.to_datetime(perf_df['date'])
            fig_perf = px.line(perf_df, x='date', y=['current_value', 'invested'], title='Value vs. Investment Over Time')
            fig_perf.update_layout(yaxis_title="Amount (₹)")
            st.plotly_chart(fig_perf, use_container_width=True)
        else:
            st.info("No snapshot history to display growth. Create a snapshot to start tracking.")


st.markdown("---")

# --- RECENT ACTIVITY & ACTIONS ---
activity_col, actions_col = st.columns([3, 1])

with activity_col:
    st.subheader("Recent Transactions")
    if recent_txn:
        txn_df = pd.DataFrame(recent_txn)
        st.dataframe(txn_df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions found.")

with actions_col:
    st.subheader("Quick Actions")
    if st.button("Add Transaction", use_container_width=True):
        st.switch_page("pages/3_💰_Transactions.py")

    # Placeholder for price refresh
    if st.button("Refresh Prices", use_container_width=True, disabled=True):
        st.toast("Price refresh feature coming soon!")

    if st.button("Create Snapshot", use_container_width=True):
        success, message = create_snapshot(user_id)
        if success:
            st.toast(message, icon="✅")
            st.experimental_rerun()
        else:
            st.toast(message, icon="⚠️")

    if st.button("View Full Portfolio", use_container_width=True):
        st.switch_page("pages/2_💼_Portfolio.py")