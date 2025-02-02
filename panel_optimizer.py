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
    return total_pieces, fit_horizontally, fit_vertically, remaining_area, waste_percentage, remaining_width, remaining_height

def visualize_cutting(main_width, main_height, cut_width, cut_height, fit_horizontally, fit_vertically, remaining_width, remaining_height):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, main_width)
    ax.set_ylim(0, main_height)
    ax.set_xticks(np.arange(0, main_width+1, cut_width))
    ax.set_yticks(np.arange(0, main_height+1, cut_height))
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    # Draw main panel
    ax.add_patch(plt.Rectangle((0, 0), main_width, main_height, fill=False, edgecolor='black', linewidth=2, label="Main Panel"))
    
    # Draw cut panels
    for i in range(fit_horizontally):
        for j in range(fit_vertically):
            ax.add_patch(plt.Rectangle((i * cut_width, j * cut_height), cut_width, cut_height, fill=True, color='lightblue', edgecolor='black'))
    
    # Draw remaining areas
    if remaining_width > 0:
        ax.add_patch(plt.Rectangle((fit_horizontally * cut_width, 0), remaining_width, main_height, fill=True, color='red', alpha=0.5, label="Waste Area"))
    if remaining_height > 0:
        ax.add_patch(plt.Rectangle((0, fit_vertically * cut_height), main_width, remaining_height, fill=True, color='red', alpha=0.5))
    
    ax.legend(loc="upper right", fontsize="small")
    ax.set_title(f"Cutting Layout")
    plt.xlabel("Width (cm)")
    plt.ylabel("Height (cm)")
    st.pyplot(fig)

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
        total_pieces, fit_horizontally, fit_vertically, remaining_area, waste_percentage, remaining_width, remaining_height = calculate_cutting_layout(
            main_width, main_height, cut_width, cut_height)
        
        visualize_cutting(main_width, main_height, cut_width, cut_height, fit_horizontally, fit_vertically, remaining_width, remaining_height)
        
    # Display saved inventory data
    st.write("### Saved Panel Data (Inventory)")
    if saved_data:
        for entry in saved_data:
            st.write(entry)
    else:
        st.write("No saved data yet.")

if __name__ == "__main__":
    main()
