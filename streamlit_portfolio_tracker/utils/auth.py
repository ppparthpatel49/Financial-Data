import streamlit as st
import bcrypt
from database.db import SessionLocal
from database.models import User

def check_authentication():
    """
    Checks if the user is authenticated by verifying session state.
    Initializes session state variables if they don't exist.
    """
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state.authenticated

def show_login_page():
    """
    Displays the login and registration form.
    """
    st.title("Welcome to Portfolio Tracker")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if authenticate_user(email, password):
                    st.success("Logged in successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid email or password.")

    with register_tab:
        with st.form("register_form"):
            name = st.text_input("Name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                if password != confirm_password:
                    st.error("Passwords do not match.")
                elif register_user(name, email, password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Email already registered.")

def authenticate_user(email, password):
    """
    Authenticates a user by checking the email and password against the database.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            st.session_state.authenticated = True
            st.session_state.user = {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            return True
        return False
    finally:
        db.close()

def register_user(name, email, password):
    """
    Registers a new user in the database.
    """
    db = SessionLocal()
    try:
        # Check if user already exists
        if db.query(User).filter(User.email == email).first():
            return False

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Create new user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password.decode('utf-8')
        )
        db.add(new_user)
        db.commit()
        return True
    finally:
        db.close()

def logout_user():
    """
    Logs out the user by clearing the session state.
    """
    st.session_state.authenticated = False
    st.session_state.user = None
    st.experimental_rerun()