import requests
import streamlit as st

API_URL = "https://www.carboninterface.com/api/v1"

HEADERS = {
    "Authorization": f"Bearer {st.secrets['CARBON_API_KEY']}",
    "Content-Type": "application/json"
}

def estimate_electricity_emissions(kwh, country="us"):
    try:
        data = {
            "type": "electricity",
            "electricity_unit": "kwh",
            "electricity_value": kwh,
            "country": country
        }
        response = requests.post(f"{API_URL}/estimates", json=data, headers=HEADERS)
        response.raise_for_status()  
      
        # handle response 
        json_data = response.json()
        if isinstance(json_data, list) and len(json_data) > 0:
            json_data = json_data[0]  # Take the first item in the list
        carbon_kg = json_data.get("data", {}).get("attributes", {}).get("carbon_kg")
        if carbon_kg is not None:
            return carbon_kg
        else:
            raise ValueError("Missing 'carbon_kg' in API response")
    except (requests.exceptions.HTTPError, ValueError, Exception) as e:
       
        return round(kwh * 0.5, 2)  #fallback 

def estimate_vehicle_emissions(distance_km, vehicle_model_id):
    try:
        data = {
            "type": "vehicle",
            "distance_unit": "km",
            "distance_value": distance_km,
            "vehicle_model_id": vehicle_model_id  
        }
        response = requests.post(f"{API_URL}/estimates", json=data, headers=HEADERS)
        response.raise_for_status()

        # handle response
        json_data = response.json()
        if isinstance(json_data, list) and len(json_data) > 0:
            json_data = json_data[0]  
        carbon_kg = json_data.get("data", {}).get("attributes", {}).get("carbon_kg")
        if carbon_kg is not None:
            return carbon_kg
        else:
            raise ValueError("Missing 'carbon_kg' in API response")
    except (requests.exceptions.HTTPError, ValueError, Exception) as e:
       
        return round(distance_km * 0.1, 2)  # fallback
