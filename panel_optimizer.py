import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calculate_cutting_layout(main_width, main_height, cut_width, cut_height):
    fit_horizontally = main_width // cut_width
    fit_vertically = main_height // cut_height
    total_pieces = fit_horizontally * fit_vertically
    remaining_width = main_width - (fit_horizontally * cut_width)
    remaining_height = main_height - (fit_vertically * cut_height)
    remaining_area = (remaining_width * main_height) + (remaining_height * main_width) - (remaining_width * remaining_height)
    return total_pieces, fit_horizontally, fit_vertically, remaining_area

def visualize_cutting(main_width, main_height, cut_width, cut_height):
    total_pieces, fit_horizontally, fit_vertically, remaining_area = calculate_cutting_layout(
        main_width, main_height, cut_width, cut_height)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, main_width)
    ax.set_ylim(0, main_height)
    ax.set_xticks(np.arange(0, main_width+1, cut_width))
    ax.set_yticks(np.arange(0, main_height+1, cut_height))
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    ax.add_patch(plt.Rectangle((0, 0), main_width, main_height, fill=False, edgecolor='black', linewidth=2))
    
    for i in range(fit_horizontally):
        for j in range(fit_vertically):
            ax.add_patch(plt.Rectangle((i * cut_width, j * cut_height), cut_width, cut_height, fill=True, color='lightblue', edgecolor='black'))
    
    ax.set_title(f"Cutting Layout: {total_pieces} pieces fit")
    plt.xlabel("Width (cm)")
    plt.ylabel("Height (cm)")
    st.pyplot(fig)

def main():
    st.title("Panel Cutting Optimizer")
    
    # Inputs
    main_width = st.number_input("Enter the width of the main panel (cm):", min_value=1)
    main_height = st.number_input("Enter the height of the main panel (cm):", min_value=1)
    cut_width = st.number_input("Enter the width of the cut panel (cm):", min_value=1)
    cut_height = st.number_input("Enter the height of the cut panel (cm):", min_value=1)
    quantity_main_panels = st.number_input("Enter the quantity of main panels:", min_value=1)
    cost_per_sqm = st.number_input("Enter the cost per square meter (€):", min_value=0.0, format="%.2f")
    additional_costs = st.number_input("Enter additional costs (e.g., transport) (€):", min_value=0.0, format="%.2f")
    discard_percentage_panels = st.number_input("Enter discarded panels percentage (due to defects):", min_value=0.0, max_value=100.0, format="%.2f")
    cutting_waste_percentage = st.number_input("Enter cutting waste percentage (from processing):", min_value=0.0, max_value=100.0, format="%.2f")

    if st.button("Generate Cutting Layout"):
        total_pieces, fit_horizontally, fit_vertically, remaining_area = calculate_cutting_layout(
            main_width, main_height, cut_width, cut_height)
        
        # Calculations
        total_smaller_panels = total_pieces * quantity_main_panels
        discard_factor = (100 - discard_percentage_panels) / 100  # Retain only good panels
        total_good_panels = total_smaller_panels * discard_factor

        main_panel_area = main_width * main_height / 10000  # Convert to sqm
        total_main_panel_area = main_panel_area * quantity_main_panels

        cutting_waste_factor = (100 - cutting_waste_percentage) / 100
        effective_main_panel_area = total_main_panel_area * cutting_waste_factor

        cost_per_main_panel = cost_per_sqm * main_panel_area
        total_cost = (cost_per_main_panel * quantity_main_panels) + additional_costs
        adjusted_total_cost = total_cost / cutting_waste_factor  # Adjust for waste cost
        cost_per_good_panel = adjusted_total_cost / total_good_panels

        cut_panel_area = cut_width * cut_height / 10000  # Area of each smaller panel in sqm
        cost_per_sqm_of_smaller_panel = cost_per_good_panel / cut_panel_area

        # Outputs
        st.write(f"### Results")
        st.write(f"Total quantity of smaller panels (before discard): **{total_smaller_panels}**")
        st.write(f"Total good panels (after defects): **{int(total_good_panels)}**")
        st.write(f"Remaining unused area (per main panel): **{remaining_area / 10000:.2f} sqm**")
        st.write(f"Cost per square meter (of smaller panel): **€{cost_per_sqm_of_smaller_panel:.2f}**")
        st.write(f"Cost per single good panel: **€{cost_per_good_panel:.2f}**")
        st.write(f"Total cost (including additional costs and cutting waste): **€{adjusted_total_cost:.2f}**")
        
        visualize_cutting(main_width, main_height, cut_width, cut_height)

if __name__ == "__main__":
    main()
