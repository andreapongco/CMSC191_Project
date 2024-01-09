import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Read the Excel file
file_path = 'Dataset-Saleh-et-al.csv'
data = pd.read_csv(file_path)

# Extract columns related to Pyrms
pyrm_columns = data.columns[5:]

# Function to plot stacked bar graph
def plot_graph(selected_pyrm):
    if selected_pyrm:
        pyrm_data = data[['country', selected_pyrm]]
        pyrm_types = sorted(pyrm_data[selected_pyrm].unique())
        
        # Replace 0 values with 'Missing Data' label
        pyrm_types = ['Missing Data' if pyrm_type == 0 else pyrm_type for pyrm_type in pyrm_types]
        
        country_counts = []

        for pyrm_type in pyrm_types:
            country_counts.append(pyrm_data.groupby('country')[selected_pyrm].apply(lambda x: (x == pyrm_type).sum()))

        plt.figure(figsize=(12, 6))
        plt.bar(range(len(country_counts[0])), country_counts[0], label=f'Pyrm Length {pyrm_types[0]}')

        for i in range(1, len(country_counts)):
            plt.bar(range(len(country_counts[i])), country_counts[i],
                    bottom=[sum(x) for x in zip(*country_counts[:i])],
                    label=f'Pyrm Length {pyrm_types[i]}')

        plt.xlabel('Countries')
        plt.ylabel(f'Counts of Pyrm Types for {selected_pyrm}')
        plt.title(f'Counts of Different Pyrm Lengths for {selected_pyrm} across Countries')
        plt.xticks(range(len(country_counts[0])), country_counts[0].index, rotation=45)
        plt.legend(title='Pyrm Types')
        plt.tight_layout()
        plt.show()

root = tk.Tk()
root.title("Pyrm Types Counts per Country")

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
