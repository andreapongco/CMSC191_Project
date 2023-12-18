import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk


# Read the Excel file
file_path = 'Dataset-Saleh-et-al.xlsx'
data = pd.read_excel(file_path)

# Calculate the total count per pyrm
pyrm_columns = data.columns[5:]
data[pyrm_columns] = data[pyrm_columns].apply(pd.to_numeric, errors='coerce')

total_per_pyrm = data[pyrm_columns].sum()

# Calculate percentages per country for each pyrm
countries = data['country'].unique()
country_percentages = []

for country in countries:
    country_data = data[data['country'] == country]
    country_totals = country_data[pyrm_columns].sum()
    country_percentage = country_totals / total_per_pyrm * 100
    country_percentage.name = country
    country_percentages.append(country_percentage)

# Important parts start here
def plot_graph(selected_value):
    if selected_value:
        plt.figure(figsize=(8, 6))
        for i, country_percentage in enumerate(country_percentages):
            plt.bar(i, country_percentage[selected_value], label=country_percentage.name)

        plt.xlabel('Countries')
        plt.ylabel('Percentage')
        plt.title(f'Percentage per Country for {selected_value}')
        plt.xticks(range(len(countries)), countries)
        plt.legend()
        plt.tight_layout()
        plt.show()

root = tk.Tk()
root.title("Pyrm Percentage per Country")

selected_pyrm = tk.StringVar()
pyrm_label = ttk.Label(root, text="Select Pyrm:")
pyrm_label.pack()

pyrm_dropdown = ttk.Combobox(root, textvariable=selected_pyrm)
pyrm_dropdown['values'] = tuple(pyrm_columns)
pyrm_dropdown.pack()

def plot_wrapper():
    selected_value = selected_pyrm.get()
    plot_graph(selected_value)

plot_button = ttk.Button(root, text="Plot", command=plot_wrapper)
plot_button.pack()

root.mainloop()
