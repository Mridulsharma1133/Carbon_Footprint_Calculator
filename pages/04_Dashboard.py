import streamlit as st
import pandas as pd
import time

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("Please login first to access this page.")
    st.stop()

user_email = st.session_state["user"]["email"]
st.write(f"Welcome, {user_email} ")


st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# step 1 : Session check
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("Please log in first to access the dashboard")
    st.stop()

# Step 2 : Greeting and layout
st.title("Welcome to your carbon footprint dashboard")
st.write(f"Hello, **{st.session_state['user']['email']}**")

st.divider()

# step 3 : Placeholder cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total CO₂ Emission", "0.0", "tonnes/year")
col2.metric("Electricity", "0.0", "tonnes/year")
col3.metric("Transportation", "0.0", "tonnes/year")
col4.metric("Diet", "0.0", "tonnes/year")


# Step 4 : Dummy Data for Graph
# Later it will change
st.subheader("Email Trends (sample)")
data = pd.DataFrame({
    "Months": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Emission": [1.2, 1.5, 1.3, 1.8, 1.6],
})
st.line_chart(data, x = "Months", y = "Emission")\

# step 5 : future sections placeholder
with st.expander("Personalized AI tips (coming soon)"):
    st.info("AI suggestions will appear here after integrating your ML Model.")

