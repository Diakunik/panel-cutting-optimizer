import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def calculate_cutting_layout(main_width, main_height, cut_width, cut_height):
    fit_horizontally = main_width // cut_width
    fit_vertically = main_height // cut_height
    total_pieces = fit_horizontally * fit_vertically
    remaining_width = main_width - (fit_horizontally * cut_width)
    remaining_height = main_height - (fit_vertically * cut_height)
    remaining_area = (remaining_width * main_height) + (remaining_height * main_width) - (remaining_width * remaining_height)
    total_main_area = main_width * main_height
    waste_percentage = (remaining_area / total_main_area) * 100  # Calculate waste percentage
    return total_pieces, fit_horizontally, fit_vertically, remaining_area, waste_percentage

def visualize_cutting(main_width, main_height, cut_width, cut_height, fit_horizontally, fit_vertically, remaining_width, remaining_height):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(0, main_width)
    ax.set_ylim(0, main_height)
    ax.set_xticks(np.arange(0, main_width+1, cut_width))
    ax.set_yticks(np.arange(0, main_height+1, cut_height))
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    # Set background color to mimic paper texture
    ax.set_facecolor("#f5f5dc")  # Light beige color like paper
    
    # Draw main panel with a paper-like texture
    ax.add_patch(plt.Rectangle((0, 0), main_width, main_height, fill=True, edgecolor='black', linewidth=2, facecolor='#e6d5b8', label="Main Panel"))
    
    # Draw good panels with a slightly darker shade
    for i in range(fit_horizontally):
        for j in range(fit_vertically):
            ax.add_patch(plt.Rectangle((i * cut_width, j * cut_height), cut_width, cut_height, fill=True, color='#d4af8f', edgecolor='black'))

    # Draw remaining areas as waste
    if remaining_width > 0:
        ax.add_patch(plt.Rectangle((fit_horizontally * cut_width, 0), remaining_width, main_height, fill=True, color='#c4a484', alpha=0.5, label="Waste Area"))
    if remaining_height > 0:
        ax.add_patch(plt.Rectangle((0, fit_vertically * cut_height), main_width, remaining_height, fill=True, color='#c4a484', alpha=0.5))

    # Add legend
    ax.legend(loc="upper right", fontsize="small")
    
    ax.set_title(f"Cutting Layout - Paper Style")
    plt.xlabel("Width (cm)")
    plt.ylabel("Height (cm)")
    st.pyplot(fig)

def main():
    st.title("Panel Cutting Optimizer")
    st.markdown("""### Instructions:
    1. Enter the dimensions of your main panel and smaller panels.
    2. Provide the cost and quantity details.
    3. Click **Generate Cutting Layout** to see results.
    """)
    
    # Inputs
    st.markdown("### Panel Dimensions")
    main_width = st.number_input("Enter the width of the main panel (cm):", min_value=1)
    main_height = st.number_input("Enter the height of the main panel (cm):", min_value=1)
    cut_width = st.number_input("Enter the width of the cut panel (cm):", min_value=1)
    cut_height = st.number_input("Enter the height of the cut panel (cm):", min_value=1)

    st.markdown("### Costs and Quantities")
    quantity_main_panels = st.number_input("Enter the quantity of main panels:", min_value=1)
    cost_per_sqm = st.number_input("Enter the cost per square meter (€):", min_value=0.0, format="%.2f")
    additional_costs = st.number_input("Enter additional costs (e.g., transport) (€):", min_value=0.0, format="%.2f")
    discard_percentage_panels = st.number_input("Enter discarded panels percentage (due to defects):", min_value=0.0, max_value=100.0, format="%.2f")

    if st.button("Generate Cutting Layout"):
        total_pieces, fit_horizontally, fit_vertically, remaining_area, waste_percentage = calculate_cutting_layout(
            main_width, main_height, cut_width, cut_height)
        
        # Calculations
        total_smaller_panels = total_pieces * quantity_main_panels
        discard_factor = (100 - discard_percentage_panels) / 100  # Retain only good panels
        total_good_panels = total_smaller_panels * discard_factor

        main_panel_area = main_width * main_height / 10000  # Convert to sqm
        total_main_panel_area = main_panel_area * quantity_main_panels

        effective_main_panel_area = total_main_panel_area * ((100 - waste_percentage) / 100)

        cost_per_main_panel = cost_per_sqm * main_panel_area
        total_cost = (cost_per_main_panel * quantity_main_panels) + additional_costs
        adjusted_total_cost = total_cost / ((100 - waste_percentage) / 100)  # Adjust for waste cost
        cost_per_good_panel = adjusted_total_cost / total_good_panels

        cut_panel_area = cut_width * cut_height / 10000  # Area of each smaller panel in sqm
        cost_per_sqm_of_smaller_panel = cost_per_good_panel / cut_panel_area

        # Outputs
        st.markdown("### Results")
        st.write(f"Total quantity of smaller panels (before discard): **{total_smaller_panels}**")
        st.write(f"Total good panels (after defects): **{int(total_good_panels)}**")
        st.write(f"Remaining unused area (per main panel): **{remaining_area / 10000:.2f} sqm**")
        st.write(f"Cutting waste percentage: **{waste_percentage:.2f}%**")
        st.write(f"Cost per square meter (of smaller panel): **€{cost_per_sqm_of_smaller_panel:.2f}**")
        st.write(f"Cost per single good panel: **€{cost_per_good_panel:.2f}**")
        st.write(f"Total cost (including additional costs and cutting waste): **€{adjusted_total_cost:.2f}**")

        # Visualize layout with paper effect
        visualize_cutting(main_width, main_height, cut_width, cut_height, fit_horizontally, fit_vertically, main_width - fit_horizontally * cut_width, main_height - fit_vertically * cut_height)

if __name__ == "__main__":
    main()
