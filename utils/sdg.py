def get_sdg_alignment(data):
    """
    Impact areas to UN SDGs
    """
    aligned_sdgs = set()

    # SDG 12 – Waste reduction, responsible use
    if data["waste_emissions"] < 5 or data["recycle_types"]:
        aligned_sdgs.add("♻️ SDG 12: Responsible Consumption & Production")

    # SDG 13 – Climate action (low CO₂, avoided travel)
    if data["total_footprint"] < 300 or data["digital_impact"] > 1:
        aligned_sdgs.add("🌍 SDG 13: Climate Action")

    # SDG 9 – Digital innovation (cards shared, travel saved)
    if data["cards_shared"] >= 5 or data["travel_saved_km"] > 10:
        aligned_sdgs.add("🏗️ SDG 9: Industry, Innovation & Infrastructure")

    # SDG 17 – Collaboration (shared cards + digital meetings)
    if data["cards_shared"] > 10 and data["meetings_held"] > 3:
        aligned_sdgs.add("🤝 SDG 17: Partnerships for the Goals")

    return list(aligned_sdgs) or ["No strong SDG alignment detected"]
