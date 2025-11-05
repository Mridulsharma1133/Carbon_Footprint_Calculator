import streamlit as st
from auth.auth_utils import register_user, login_user, logout_user
import supabase

def clean_error(err):
    """Remove or convert any non-ASCII characters in error messages."""
    if not err:
        return ""
    try:
        return str(err).encode("utf-8", errors="ignore").decode("utf-8")
    except Exception:
        return "An unknown error occurred."

st.set_page_config(
    page_title="AI Carbon Calculator",
    layout="wide"
)
st.title(" Welcome to the AI Carbon Footprint App")

# session state initialization
if "user" not in st.session_state:
    st.session_state["user"] = None

# if user already logged in, show dashboard link
if st.session_state['user']:
    st.sidebar.success(f'Logged in as: {st.session_state['user']['email']}')
    if st.sidebar.button("Logout"):
        logout_user()
        st.session_state['user'] = None
        st.rerun()

else:
    # Tabs for login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])


    # Login Tab
    with tab1:
        st.subheader("Login to your account")

        email = st.text_input("Email", key='login_email')
        password = st.text_input("Password", type = "password", key="login_password")

        if st.button('Login'):
            user, error = login_user(email, password)
            if error:
                st.error(f"Login failed: {clean_error(error)}")
            
            else:
                st.session_state["user"] = {"email":email}
                st.success("Login successful! Redirecting...")
                st.rerun()
        
    # Register Tab
    with tab2:
        st.subheader("Create a new account")

        reg_email = st.text_input("Email", key="register_email")
        reg_password = st.text_input("Password",type="password")

        if st.button("Register"):
            user, error = register_user(reg_email, reg_password)
            if error:
                st.error(f"Registration failed: {clean_error(error)}")
            else:
                st.success("Registration successful! Please log in.")
