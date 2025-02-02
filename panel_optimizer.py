import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def calculate_cutting_layout(main_width, main_height, cut_width, cut_height):
    fit_horizontally = main_width // cut_width
    fit_vertically = main_height // cut_height
    total_pieces = fit_horizontally * fit_vertically
    remaining_width = main_width - (fit_horizontally * cut_width)
    remaining_height = main_height - (fit_vertically * cut_height)
    return total_pieces, fit_horizontally, fit_vertically, remaining_width, remaining_height

def visualize_cutting(main_width, main_height, cut_width, cut_height):
    total_pieces, fit_horizontally, fit_vertically, remaining_width, remaining_height = calculate_cutting_layout(
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
    
    if remaining_width > 0:
        ax.add_patch(plt.Rectangle((fit_horizontally * cut_width, 0), remaining_width, main_height, fill=True, color='lightgrey', edgecolor='black'))
    if remaining_height > 0:
        ax.add_patch(plt.Rectangle((0, fit_vertically * cut_height), main_width, remaining_height, fill=True, color='lightgrey', edgecolor='black'))
    
    ax.set_title(f"Cutting Layout: {total_pieces} pieces fit")
    plt.xlabel("Width (cm)")
    plt.ylabel("Height (cm)")
    st.pyplot(fig)

def main():
    st.title("Panel Cutting Optimizer")
    
    main_width = st.number_input("Enter the width of the main panel (cm):", min_value=1)
    main_height = st.number_input("Enter the height of the main panel (cm):", min_value=1)
    cut_width = st.number_input("Enter the width of the cut panel (cm):", min_value=1)
    cut_height = st.number_input("Enter the height of the cut panel (cm):", min_value=1)
    
    if st.button("Generate Cutting Layout"):
        visualize_cutting(main_width, main_height, cut_width, cut_height)
    
if __name__ == "__main__":
    main()
