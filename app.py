import streamlit as st
from datetime import datetime
from utils.genai import generate_impact_summary
from utils.sdg import get_sdg_alignment
from utils.storage import save_report, fetch_user_logs
from utils.carbon_api import estimate_electricity_emissions, estimate_vehicle_emissions


# ------------------------
# Page Configuration

st.set_page_config(page_title="Eco-Focus", layout="centered")
st.title("🌍 Eco-Focus")
st.caption("Understand your impact. Inspire sustainable action.")

st.image("https://www.ecofocus.ltd/wp-content/uploads/2023/02/earth-gc0158472e_1920-e1676455731679.png", use_container_width=True)
st.markdown("""
Welcome to **Eco-Focus**, your personal eco -assistant.

Together, we’re building a greener planet by tracking real environmental impact — 
from trees planted 🌱 to carbon emissions reduced 🌫️. Whether you're a citizen scientist, 
a farm owner, or a sustainability team — you’ll find insights here that matter.

👉 Start by exploring your region's impact, monitoring trends, and getting inspired to act.


## Why Eco-Focus?

Tracking and reducing your carbon footprint just got simpler.  
**Eco-Focus** turns your digital actions into measurable environmental impact — from **paper saved** to **CO₂ reduced**, and aligns your efforts with the **UN Sustainable Development Goals (SDGs)**.

💡 *It’s personal, actionable, and inspiring.*

""")

# ------------------------
# Sidebar Inputs

st.sidebar.header("Your Activity")
user_type = st.sidebar.selectbox("Who are you?", ["Individual", "Business"])
nickname = st.sidebar.text_input("Your Name or Nickname")
region = st.sidebar.text_input("Your Region (e.g., India,USA)")


cards_shared = st.sidebar.number_input("Cards Shared Digitally", min_value=0)
meetings_held = st.sidebar.number_input("Digital Meetings Held", min_value=0)
paper_cards_avoided = st.sidebar.number_input("Paper Business Cards Avoided", min_value=0)
travel_saved_km = st.sidebar.number_input("Business Travel Avoided (km)", min_value=0)

st.sidebar.markdown("---")
st.sidebar.header("♻️ Lifestyle Inputs")

energy_usage = st.sidebar.number_input("Monthly Energy Use (kWh)", min_value=0.0, step=1.0)
renewable_ratio = st.sidebar.slider("Renewable Energy Usage (%)", 0, 100, 20)

water_consumption = st.sidebar.number_input("Monthly Water Use (liters)", min_value=0.0, step=10.0)
commute_distance = st.sidebar.number_input("Weekly Commute Distance (km)", min_value=0.0, step=1.0)
transport_mode = st.sidebar.selectbox("Transport Mode", ["Car", "Bike", "Bus", "Train", "Electric Vehicle"])

weekly_waste = st.sidebar.number_input("Weekly Waste Generated (kg)", min_value=0.0, step=0.1)
recycle_types = st.sidebar.multiselect("Recycled Materials", ["Plastic", "Glass", "Paper", "E-waste", "Other"])

# ------------------------
# Emissions Calculation Helpers

def calculate_commute_emissions(distance_km, mode):
    emission_factors = {
        "Car": 0.21, "Bike": 0.05, "Bus": 0.089, "Train": 0.041, "Electric Vehicle": 0.06
    }
    return distance_km * emission_factors.get(mode, 0.1)

def calculate_energy_emissions(kwh):
    return kwh * 0.5

def calculate_water_emissions(liters):
    return liters * 0.0003

def calculate_waste_emissions(kg):
    return kg * 1.8

# ------------------------
# Report Generation Logic

if st.sidebar.button("Generate Impact Report"):
    st.session_state["trigger"] = True

    # Calculations
    country_code = region.lower().strip()[:2] if region else "us"
    energy_emissions = estimate_electricity_emissions(energy_usage, country=country_code)

    commute_emissions = calculate_commute_emissions(commute_distance, transport_mode)

    water_emissions = calculate_water_emissions(water_consumption)
    waste_emissions = calculate_waste_emissions(weekly_waste)

    total_footprint = energy_emissions + commute_emissions + water_emissions + waste_emissions
    digital_impact = cards_shared * 0.02 + travel_saved_km * 0.1

    # SDG Alignment
    sdg_input = {
        "waste_emissions": waste_emissions,
        "recycle_types": recycle_types,
        "total_footprint": total_footprint,
        "digital_impact": digital_impact,
        "cards_shared": cards_shared,
        "travel_saved_km": travel_saved_km,
        "meetings_held": meetings_held
    }
    aligned_sdgs = get_sdg_alignment(sdg_input)

    # ------------------------
    # Display Report

    st.subheader("🌿 Your Estimated Carbon Impact (kg CO₂)")
    st.metric("Total Estimated Footprint", f"{total_footprint:.2f} kg CO₂")

    st.markdown("### 📜 Category Breakdown")
    st.dataframe({
        "Category": ["Energy", "Water", "Commute", "Waste"],
        "CO₂ Emissions (kg)": [
            round(energy_emissions, 2),
            round(water_emissions, 2),
            round(commute_emissions, 2),
            round(waste_emissions, 2)
        ]
    })

    st.markdown("### ♻️ Recycling Efforts")
    if recycle_types:
        st.success(f"You are recycling: {', '.join(recycle_types)}")
    else:
        st.warning("No recycling options selected.")

    st.markdown("### 📊 Digital Savings Impact")
    st.write(
        f"Thanks to your digital habits, you've helped avoid approximately **{digital_impact:.2f} kg CO₂** via digital cards and reduced travel.")

    st.markdown("### 🌐 SDG Alignment")
    if isinstance(aligned_sdgs, list):
        for sdg in aligned_sdgs:
            if isinstance(sdg, dict):
                goal = sdg.get("goal", "?")
                description = sdg.get("description", "No description available.")
                st.success(f"✅ SDG {goal}: {description}")
            else:
                st.warning(f"*: {sdg}")
    else:
        st.info("Your current impact doesn't match any SDG indicators yet. Keep going!")

    # AI Impact Summary
    st.markdown("### 🤖 AI-Powered Sustainability Summary")
    input_data = {
        "nickname": nickname or "User",
        "region": region or "Global",
        "user_type": user_type,
        "energy_emissions": round(energy_emissions, 2),
        "commute_emissions": round(commute_emissions, 2),
        "transport_mode": transport_mode,
        "water_consumption": round(water_consumption, 2),
        "waste_emissions": round(waste_emissions, 2),
        "recycle_types": ", ".join(recycle_types) if recycle_types else "None",
        "cards_shared": cards_shared,
        "travel_saved_km": travel_saved_km,
        "digital_impact": round(digital_impact, 2)
    }

    with st.spinner("Generating personalized impact summary..."):
        try:
            summary = generate_impact_summary(input_data)
            st.success("Here’s your eco-impact report:")
            st.write(summary)
        except Exception as e:
            st.error(f"Failed to generate summary: {e}")



    # SAVE REPORT
    save_data = {
        "timestamp": datetime.now().isoformat(),
        "nickname": nickname,
        "user_type": user_type,
        "region": region,
        "cards_shared": cards_shared,
        "meetings_held": meetings_held,
        "paper_cards_avoided": paper_cards_avoided,
        "travel_saved_km": travel_saved_km,
        "energy_emissions": energy_emissions,
        "commute_emissions": commute_emissions,
        "water_emissions": water_emissions,
        "waste_emissions": waste_emissions,
        "digital_impact": digital_impact,
        "total_footprint": total_footprint
    }

    try:
        save_report(save_data)
        st.success("✅ Your report has been saved.")
    except Exception as e:
        st.error(f"⚠️ Failed to save report: {e}")

        # Display previous logs
    st.markdown("### 🕓 Your Previous Reports")
    logs = fetch_user_logs(nickname)
    if logs:
        import pandas as pd

        df = pd.DataFrame(logs)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(df[[
            "timestamp", "total_footprint", "digital_impact", "cards_shared", "waste_emissions"
        ]])
    else:
        st.info("No previous logs found for this nickname.")