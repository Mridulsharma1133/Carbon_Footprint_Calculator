import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Register / Login", layout="wide")
st.title(" Register or Login")

os.makedirs("data", exist_ok=True)
users_file = "data/users.csv"

if not os.path.exists(users_file):
    pd.DataFrame(columns=["email", "password"]).to_csv(users_file, index=False)

tab1, tab2 = st.tabs([" Login", " Register"])

# Login
with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = pd.read_csv(users_file)
        if ((users["email"] == email) & (users["password"] == password)).any():
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email
            st.success("Login successful!")
        else:
            st.error(" Invalid credentials")

# Register
with tab2:
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        users = pd.read_csv(users_file)
        if new_email in users["email"].values:
            st.warning("User already exists")
        else:
            new_row = pd.DataFrame([[new_email, new_password]], columns=["email", "password"])
            new_row.to_csv(users_file, mode='a', header=False, index=False)
            st.success(" Registered successfully! Please login.")


