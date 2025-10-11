import streamlit as st
from streamlit_option_menu import option_menu
from database.init_db import init_database
from utils.auth import check_authentication, show_login_page, logout_user
# from services.portfolio_service import get_portfolio_summary # Will be implemented later

def main():
    """
    Main function to run the Streamlit application.
    """
    st.set_page_config(
        page_title="Portfolio Tracker",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize the database
    try:
        init_database()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop()

    # Check authentication
    if not check_authentication():
        show_login_page()
        st.stop()

    # --- Main Application UI ---

    # Custom CSS for styling
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 2rem;
            }
            .st-emotion-cache-16txtl3 {
                padding-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title(f"Welcome, {st.session_state.user['name']}!")

        # --- Placeholder for Quick Stats ---
        # summary = get_portfolio_summary(st.session_state.user['id'])
        # st.metric("Portfolio Value", f"₹{summary['current_value']:,.2f}")
        # st.metric("Total Gain", f"₹{summary['total_gain']:,.2f}", delta=f"{summary['gain_percent']:.2f}%")
        st.info("Quick stats will be shown here.")

        st.markdown("---")

        # Navigation Menu
        # The pages are automatically loaded by Streamlit from the `pages/` directory.
        # This menu will be for show or for controlling the main view if not using multipage app feature directly.
        # For now, we assume Streamlit's native multipage app handling is sufficient.
        st.page_link("app.py", label="Home / Login", icon="🏠")
        st.page_link("pages/1_📊_Dashboard.py", label="Dashboard", icon="📊")
        st.page_link("pages/2_💼_Portfolio.py", label="Portfolio", icon="💼")
        st.page_link("pages/3_💰_Transactions.py", label="Transactions", icon="💰")
        st.page_link("pages/4_🎯_Goals.py", label="Goals", icon="🎯")
        st.page_link("pages/5_📈_PE_Matrix.py", label="PE Matrix", icon="📈")
        st.page_link("pages/6_📉_Drawdown.py", label="Drawdown", icon="📉")
        st.page_link("pages/7_📋_Tax_Report.py", label="Tax Report", icon="📋")
        st.page_link("pages/8_⚙️_Settings.py", label="Settings", icon="⚙️")
        st.page_link("pages/9_🔔_Alerts.py", label="Alerts", icon="🔔")

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            logout_user()

    st.title("Streamlit Portfolio Tracker")
    st.write("Select a page from the sidebar to get started.")
    st.info("This is the main landing page. The actual functionality is organized into separate pages.")


if __name__ == "__main__":
    main()