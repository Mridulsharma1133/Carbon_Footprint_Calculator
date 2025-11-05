import streamlit as st
from auth.auth_utils import register_user, login_user, logout_user

st.set_page_config(page_title="Login / Register", layout='centered')
st.title("Login or Register")

# Initialize session states
if "user" not in st.session_state:
    st.session_state['user'] = None
if "session" not in st.session_state:
    st.session_state['session'] = None

# Function to safely clean error messages (fixes ascii codec issues)
def clean_error(err):
    if not err:
        return ""
    try:
        # Convert to string, then encode/decode safely ignoring weird symbols
        return str(err).encode("utf-8", errors="ignore").decode("utf-8")
    except Exception:
        return "An unknown error occurred."

# Tabs
tabs = st.tabs(["Login", "Register"])

# ------------------ LOGIN TAB ------------------
with tabs[0]:
    st.subheader("Login to your account")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        with st.spinner("Logging in..."):
            session_data, error = login_user(login_email, login_password)

        # Clean and handle error
        if error:
            safe_error = clean_error(error)
            st.error(f"Login failed: {safe_error}")
        else:
            # Store session and user info
            st.session_state["session"] = session_data
            user_email = None
            if isinstance(session_data, dict):
                if 'user' in session_data and session_data['user']:
                    user_email = session_data['user'].get('email')
                
                elif 'email' in session_data:
                    user_email = session_data['email']
            
            if user_email:
                st.session_state['user'] = {'email': user_email}
                st.session_state['is_authenticated'] = True
                st.success(f"Logged in as {user_email}")
                st.rerun()
            
            else:
                st.error("Unable to retrieve user details. Please try again.")
                
                

            


# ------------------ REGISTER TAB ------------------
with tabs[1]:
    st.subheader("Create a new account")

    reg_email = st.text_input("Email", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")

    if st.button("Register"):
        with st.spinner("Creating account..."):
            user_data, error = register_user(reg_email, reg_password)

        if error:
            safe_error = clean_error(error)
            st.error(f"Registration failed: {safe_error}")
        else:
            st.success(
                "Registered successfully! Please check your email for confirmation and then log in."
            )
