import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Home - Carbon Calculator", layout="wide", initial_sidebar_state="collapsed")
st.title(" Carbon Footprint Calculator")

EMISSION_FACTORS = {
    "India": {
        "Transportation": 0.14,   # kgCO2/km
        "Electricity": 0.82,      # kgCO2/kWh
        "Diet": 1.25,             # kgCO2/meal
        "Waste": 0.1              # kgCO2/kg
    }
}

# Country
country = st.selectbox("Select your Country", ["India"])

col1, col2 = st.columns(2)

with col1:
    distance = st.slider(" Daily commute distance (in km)", 0.0, 100.0, 20.0)
    electricity = st.slider(" Monthly electricity usage (kWh)", 0.0, 1000.0, 250.0)

with col2:
    waste = st.slider("🗑 Waste generated per week (kg)", 0.0, 100.0, 10.0)
    meals = st.number_input("Meals per day", min_value=1, max_value=10, value=3)

if st.button("Calculate CO₂ Emissions"):
    # Normalize to yearly
    distance *= 365
    electricity *= 12
    meals *= 365
    waste *= 52

    # Calculate emissions
    transportation_emission = EMISSION_FACTORS[country]['Transportation'] * distance
    electricity_emission = EMISSION_FACTORS[country]['Electricity'] * electricity
    diet_emission = EMISSION_FACTORS[country]['Diet'] * meals
    waste_emission = EMISSION_FACTORS[country]['Waste'] * waste

    # Convert to tonnes
    transportation_emission = round(transportation_emission / 1000, 2)
    electricity_emission = round(electricity_emission / 1000, 2)
    diet_emission = round(diet_emission / 1000, 2)
    waste_emission = round(waste_emission / 1000, 2)
    total_emissions = round(
        transportation_emission + electricity_emission + diet_emission + waste_emission, 2
    )

    st.subheader(" Results")

    col3, col4 = st.columns(2)
    with col3:
        st.info(f" Transportation: **{transportation_emission} tonnes/year**")
        st.info(f" Electricity: **{electricity_emission} tonnes/year**")
        st.info(f" Diet: **{diet_emission} tonnes/year**")
        st.info(f" Waste: **{waste_emission} tonnes/year**")

    with col4:
        st.success(f" **Your total footprint: {total_emissions} tonnes CO₂ per year**")

    # Save to CSV
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "country": country,
        "distance_km": distance,
        "electricity_kwh": electricity,
        "waste_kg": waste,
        "meals_per_day": meals,
        "total_emission_tonnes": total_emissions
    }

    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([record])

    file_path = "data/user_emissions.csv"
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

    st.success(" Your data has been saved for future analysis!")

