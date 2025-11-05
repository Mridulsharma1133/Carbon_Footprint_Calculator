import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
from ml_predictor import predict_emission

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please login first to access this page.")
    st.stop()

user_email = st.session_state["user"]["email"]
st.write(f"Welcome, {user_email} 👋")

# Supabase setup
url = "https://znoippfmvtxbtmeneqjd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpub2lwcGZtdnR4YnRtZW5lcWpkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEzNjYzNzEsImV4cCI6MjA3Njk0MjM3MX0.W5Dsjw53siYQ_5aOEUeMu9AYBHCuF8yfcn1btQ5ntsc"
supabase: Client = create_client(url, key)

st.title(" Carbon Footprint Calculator")

if "user" in st.session_state and st.session_state["user"]:
    user_email = st.session_state["user"]["email"]
else:
    st.warning("⚠️ Please log in to continue.")
    st.stop()

if "user" in st.session_state:
    user_email = st.session_state["user"]["email"]
else:
    user_email = None

st.write("Estimate your monthly CO2 emission (kg CO2e) based on your activities:")

col1, col2 = st.columns(2)

EMISSION_FACTORS = {
    "electricity": 0.85,
    "car":0.21,
    "bike":0.08,
    "public_transport":0.04,
    "flight":250,
    "waste":0.45,
}

DIET_FACTORS = {
    "vegetarian":125,
    "mixed":165,
    "non_vegetarian":210,
}


def calculate_carbon_footprint(electricity_kwh, car_km, bike_km, public_km, flights_per_year, diet_type, waste_kg):
    try:
        elec_emission = electricity_kwh * EMISSION_FACTORS['electricity']
        
        car_emission = car_km * EMISSION_FACTORS['car']
        bike_emission = bike_km * EMISSION_FACTORS['bike']
        public_emission = public_km * EMISSION_FACTORS['public_transport']

        flight_emission = (flights_per_year/12) * EMISSION_FACTORS["flights"]
        waste_emission = waste_kg * EMISSION_FACTORS["waste"]

        diet_emission = DIET_FACTORS.get(diet_type.lower(), 165)

        total_emission = (
            elec_emission + car_emission + bike_emission + public_emission + flight_emission + waste_emission + diet_emission
        )
        return round(total_emission,2)
    except Exception as e:
        return f"Error calculating footprint : {e}"


with col1:
    electricity_kwh = st.number_input("Electricity usage (kWh/month)",min_value=0.0, value=200.0)
    car_km = st.number_input("Car distance (km/month)", min_value=0.0, value=100.0)
    bike_km = st.number_input("Bike distance(km/month)", min_value=0.0, value=50.0)
    public_km = st.number_input("Public transport (km/month)", min_value=0.0, value=100.0)

with col2:
    flights_per_year = st.number_input("Flights per year", min_value=0, value=2)
    waste_kg = st.number_input("Waste generated (kg/month)",min_value=0.0, value=30.0)
    diet_type = st.selectbox("Diet type", ["Vegetarian", "Mixed", "Non_Vegetarian"])

if st.button("Calculate Footprint"):
    total_emission = predict_emission(
        electricity_kwh, car_km, bike_km, public_km, flights_per_year, diet_type, waste_kg
    )
    st.success(f"Your estimated monthly carbon footprint is {total_emission} kg CO₂e")

    #Save emission record
    if user_email:
        supabase.table("user_emissions").insert({
            "email": user_email,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "emission": total_emission
        }).execute()

        # Fetch and visualize emission trend
        data = supabase.table("user_emissions").select("*").eq("email", user_email).execute()
        df = pd.DataFrame(data.data)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            st.subheader("Your Emission Trend")
            st.line_chart(df.set_index('date')['emission'])
    else:
        st.warning("Please log in to save and view your emission history.")
