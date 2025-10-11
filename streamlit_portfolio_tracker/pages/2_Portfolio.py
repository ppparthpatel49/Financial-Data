import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from services.portfolio_service import get_full_portfolio, update_portfolio_from_transactions, delete_holding
from utils.auth import check_authentication
import pandas as pd

st.set_page_config(page_title="Portfolio", layout="wide")

if not check_authentication():
    st.warning("Please log in to view this page.")
    st.stop()

st.title("💼 Portfolio")

user_id = st.session_state.user['id']

# --- ACTIONS ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Refresh / Recalculate Portfolio"):
        try:
            update_portfolio_from_transactions(user_id)
            st.toast("Portfolio recalculated based on all transactions.", icon="✅")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Failed to recalculate portfolio: {e}")

with col2:
    # Placeholder for future price update feature
    st.button("Update Live Prices", disabled=True)

st.markdown("---")

# --- PORTFOLIO TABLE ---
try:
    portfolio_data = get_full_portfolio(user_id)
    if not portfolio_data:
        st.info("Your portfolio is empty. Add some transactions to see your holdings here.")
        st.stop()

    df = pd.DataFrame(portfolio_data)

    # --- AG-Grid Configuration ---
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection('single', use_checkbox=True, pre_select_all_rows=False)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()

    # Make columns editable
    # gb.configure_column("units_held", editable=True)

    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=False,
        theme='streamlit',  # or 'alpine', 'balham', 'material'
        enable_enterprise_modules=False,
        height=400,
        width='100%',
        reload_data=True
    )

    selected = grid_response['selected_rows']

    if selected:
        st.subheader("Actions for Selected Holding")
        selected_row = pd.DataFrame(selected)
        symbol = selected_row.iloc[0]['symbol']
        etf_id = selected_row.iloc[0]['etf_id']

        st.write(f"You have selected **{symbol}**.")

        if st.button(f"Delete Holding and all related data for {symbol}", type="primary"):
            st.warning(f"This is a destructive action. Are you sure you want to delete all data for {symbol}?", icon="⚠️")
            if st.button("Yes, I am sure"):
                try:
                    # Note: This is a simplified delete. A real app might need to also delete transactions.
                    if delete_holding(user_id, etf_id):
                        st.success(f"{symbol} holding deleted successfully.")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete holding.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")


except Exception as e:
    st.error(f"Failed to load portfolio data: {e}")