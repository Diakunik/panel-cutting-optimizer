import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import datetime
import json
import os

# File to store saved data
DATA_FILE = "panel_data.json"

# Function to load data from a JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save data to a JSON file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def calculate_cutting_layout(main_width, main_height, cut_width, cut_height):
    fit_horizontally = main_width // cut_width
    fit_vertically = main_height // cut_height
    total_pieces = fit_horizontally * fit_vertically
    remaining_width = main_width - (fit_horizontally * cut_width)
    remaining_height = main_height - (fit_vertically * cut_height)
    remaining_area = (remaining_width * main_height) + (remaining_height * main_width) - (remaining_width * remaining_height)
    total_main_area = main_width * main_height
    waste_percentage = (remaining_area / total_main_area) * 100
    return total_pieces, fit_horizontally, fit_vertically, remaining_area, waste_percentage

def main():
    st.title("Panel Cutting Optimizer with Inventory System")
    
    # Load saved data
    saved_data = load_data()
    
    # Inputs
    panel_name = st.text_input("Enter the panel name:")
    panel_date = st.date_input("Select the date:", datetime.date.today())
    
    main_width = st.number_input("Enter the width of the main panel (cm):", min_value=1)
    main_height = st.number_input("Enter the height of the main panel (cm):", min_value=1)
    cut_width = st.number_input("Enter the width of the cut panel (cm):", min_value=1)
    cut_height = st.number_input("Enter the height of the cut panel (cm):", min_value=1)
    quantity_main_panels = st.number_input("Enter the quantity of main panels:", min_value=1)
    cost_per_sqm = st.number_input("Enter the cost per square meter (€):", min_value=0.0, format="%.2f")
    additional_costs = st.number_input("Enter additional costs (e.g., transport) (€):", min_value=0.0, format="%.2f")
    discard_percentage_panels = st.number_input("Enter discarded panels percentage (due to defects):", min_value=0.0, max_value=100.0, format="%.2f")
    
    if st.button("Generate Cutting Layout"):
        total_pieces, fit_horizontally, fit_vertically, remaining_area, waste_percentage = calculate_cutting_layout(
            main_width, main_height, cut_width, cut_height)
        
        total_smaller_panels = total_pieces * quantity_main_panels
        discard_factor = (100 - discard_percentage_panels) / 100
        total_good_panels = total_smaller_panels * discard_factor

        main_panel_area = main_width * main_height / 10000
        total_main_panel_area = main_panel_area * quantity_main_panels
        effective_main_panel_area = total_main_panel_area * ((100 - waste_percentage) / 100)

        cost_per_main_panel = cost_per_sqm * main_panel_area
        total_cost = (cost_per_main_panel * quantity_main_panels) + additional_costs
        adjusted_total_cost = total_cost / ((100 - waste_percentage) / 100)
        cost_per_good_panel = adjusted_total_cost / total_good_panels

        cut_panel_area = cut_width * cut_height / 10000
        cost_per_sqm_of_smaller_panel = cost_per_good_panel / cut_panel_area
        
        # Save panel data to inventory
        new_entry = {
            "Panel Name": panel_name,
            "Date": str(panel_date),
            "Width": main_width,
            "Height": main_height,
            "Quantity": quantity_main_panels,
            "Cost per Sqm (€)": cost_per_sqm,
            "Total Cost (€)": adjusted_total_cost,
            "Total Smaller Panels": total_smaller_panels,
            "Good Panels After Discard": int(total_good_panels)
        }
        saved_data.append(new_entry)
        save_data(saved_data)
        
        # Display results
        st.write("### Results")
        st.write(f"Total quantity of smaller panels (before discard): **{total_smaller_panels}**")
        st.write(f"Total good panels (after defects): **{int(total_good_panels)}**")
        st.write(f"Cutting waste percentage: **{waste_percentage:.2f}%**")
        st.write(f"Cost per square meter (of smaller panel): **€{cost_per_sqm_of_smaller_panel:.2f}**")
        st.write(f"Cost per single good panel: **€{cost_per_good_panel:.2f}**")
        st.write(f"Total cost (including additional costs and cutting waste): **€{adjusted_total_cost:.2f}**")
        
    # Display saved inventory data
    st.write("### Saved Panel Data (Inventory)")
    if saved_data:
        for entry in saved_data:
            st.write(entry)
    else:
        st.write("No saved data yet.")

if __name__ == "__main__":
    main()
