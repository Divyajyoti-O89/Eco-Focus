

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Cohere
from langchain.chains import LLMChain


def generate_impact_summary(data: dict) -> str:
    # Securely access API key from secrets
    cohere_api_key = st.secrets["COHERE_API_KEY"]

    # Initialize the LLM with Cohere
    llm = Cohere(cohere_api_key=cohere_api_key)

    # Define prompt template with placeholders for user data
    prompt_template = PromptTemplate(
        input_variables=[
            "nickname", "user_type", "region", "energy_emissions", "commute_emissions",
            "water_consumption", "waste_emissions", "recycle_types", "transport_mode"
        ],
        template="""
        Generate a concise sustainability report for {nickname}, a {user_type} user based in {region}.
        
        Report structure:
        1. A brief emissions summary with key numbers:
           - Total Energy Emissions: {energy_emissions} kg CO₂
           - Total Commute Emissions: {commute_emissions} kg CO₂
           - Total Water Consumption: {water_consumption} liters
           - Total Waste Emissions: {waste_emissions} kg CO₂
        
        2. Quick Insights:
           - Highlight 2 strong areas (e.g., low water/waste, good recycling). If no strong areas are evident, mention the lowest emission categories.
           - Highlight 2 weak areas needing improvement (e.g., high energy use or poor commute mode). If no weak areas are evident, mention the highest emission categories.
        
        3. Tips to Improve:
           - Provide 2 smart, actionable tips based on the weak areas identified. Ensure the tips are specific to the user's data (e.g., if commute emissions are high and transport mode is Car, suggest switching to public transport).
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.invoke(data)
