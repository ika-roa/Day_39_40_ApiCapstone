import tkinter as tk
from tkinter import ttk
import pandas


class AppGui(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self)

        # Read starting etf df from .csv file
        self.etf_df = None
        self.etf_list = []

        # set min width for empty columns
        for index in [0, 1]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # display ETF table
        self.etf_tree = ttk.Treeview(self, columns=('ETF', 'limit'), show=["headings"])

        # set up columns
        #self.etf_tree.column('#0', width=0)
        #self.etf_tree.heading('#0', text='ETF', anchor='w')

        self.etf_tree.column('ETF', width=100, anchor='w')
        self.etf_tree.heading('ETF', text='ETF', anchor='w')

        self.etf_tree.column('limit', width=100, anchor='w')
        self.etf_tree.heading('limit', text='limit', anchor='w')

        self.display_tree()

        self.etf_tree.bind('<ButtonRelease-1>', self.select_item)
        self.etf_tree.grid(row=0, column=0, padx=5, pady=10, sticky="nsew", columnspan=2)

        # ETF Entry
        self.etf_label = ttk.Label(self, text="ETF")
        self.etf_label.grid(row=1, column=0, padx=5, pady=(0, 0), sticky="ew")

        self.etf_entry = ttk.Entry(self)
        self.etf_entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")

        # limit Entry
        self.limit_label = ttk.Label(self, text="limit")
        self.limit_label.grid(row=1, column=1, padx=5, pady=(0, 0), sticky="ew")

        self.limit_entry = ttk.Entry(self)
        self.limit_entry.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="ew")

        # Add Button
        self.add_button = ttk.Button(self, text="Add new ETF", command=self.add_new_etf)
        self.add_button.grid(row=3, column=0, padx=5, pady=10, sticky="nsew", columnspan=2)

        # Update Button
        self.update_button = ttk.Button(self, text="Update ETF", command=self.update_etf)
        self.update_button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

        # Delete Button
        self.delete_button = ttk.Button(self, text="Delete ETF", command=self.delete_etf)
        self.delete_button.grid(row=4, column=1, padx=5, pady=10, sticky="nsew")

    def display_tree(self):
        self.etf_tree.delete(*self.etf_tree.get_children())

        # Read current etfs df from .csv file
        try:
            self.etf_df = pandas.read_csv("etf_list.csv")
        except FileNotFoundError:
            self.etf_df = pandas.DataFrame(columns=['etf', 'limit'])
        self.etf_df = self.etf_df.sort_values(by=["etf"])
        # turns the dataframe into a list of lists for tree view
        self.etf_list = self.etf_df.values.tolist()

        for row in self.etf_list:
            self.etf_tree.insert("", "end", values=[row[0], row[1]])

    def select_item(self, a):
        current_item = self.etf_tree.focus()
        selected_etf = self.etf_tree.item(current_item)["values"][0]
        selected_limit = self.etf_tree.item(current_item)["values"][1]
        self.etf_entry.delete(0, 'end')
        self.etf_entry.insert(0, selected_etf)
        self.limit_entry.delete(0, 'end')
        self.limit_entry.insert(0, selected_limit)

    def add_new_etf(self):
        new_etf = self.etf_entry.get()
        new_limit = self.limit_entry.get()
        new_etf_row = {'etf': new_etf, 'limit': int(new_limit)}
        self.etf_df = self.etf_df.append(new_etf_row, ignore_index=True)
        print(self.etf_df)
        self.etf_df.to_csv("etf_list.csv", index=False)

        self.display_tree()

    def delete_etf(self):
        selected_items = self.etf_tree.selection()
        for selected_item in selected_items:
            selected_etf = self.etf_tree.item(selected_item)['values'][0]
            self.etf_df = self.etf_df[self.etf_df.etf != selected_etf]
        self.etf_df.to_csv("etf_list.csv", index=False)
        self.display_tree()

    def update_etf(self):
        self.delete_etf()
        self.add_new_etf()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("")
    root.config(padx=20, pady=20)

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = AppGui(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()