import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

class ExpenseTrackerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Braince Expense Tracker UI")
        self.root.geometry("700x500")
        self.root.configure(padx=20, pady=20)
        
        self.money = 0
        self.history = []
        self.data_file = "data.json"
        self.pin = "1234"
        
        # PIN Check - hide root until successful
        self.root.withdraw()
        if not self.check_pin():
            self.root.destroy()
            return
        self.root.deiconify()
            
        self.load_data()
        self.setup_ui()
        
    def check_pin(self):
        entered_pin = simpledialog.askstring("Login", "Enter PIN (Default is 1234):", parent=self.root, show="*")
        if entered_pin == self.pin:
            return True
        else:
            if entered_pin is not None:
                messagebox.showerror("Error", "Oops wrong PIN!")
                retry = messagebox.askyesno("Retry", "Do you want to try again?")
                if retry:
                    return self.check_pin()
            return False
        
    def load_data(self):
        try:
            with open(self.data_file, "r") as file:
                data = json.load(file)
            self.money = data.get("money", 0)
            self.history = data.get("history", [])
        except FileNotFoundError:
            self.money = 0
            self.history = []
            
    def save_data(self):
        data = {
            "money": self.money,
            "history": self.history
        }
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)
            
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Braince Expense Tracker", font=("Helvetica", 24, "bold"))
        title.pack(pady=(0, 20))
        
        # Balance Frame
        balance_frame = tk.Frame(self.root)
        balance_frame.pack(fill=tk.X, pady=10)
        
        self.balance_label = tk.Label(balance_frame, text=f"Current Balance: ${self.money}", font=("Helvetica", 18))
        self.balance_label.pack()
        
        # Action Buttons Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Buttons Row 1
        tk.Button(btn_frame, text="Add Expense", font=("Helvetica", 12), width=18, command=self.add_expense, bg="#ff6b6b", fg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Add Income", font=("Helvetica", 12), width=18, command=self.add_income, bg="#4ecdc4", fg="white").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="View History & Edit", font=("Helvetica", 12), width=18, command=self.show_history).grid(row=0, column=2, padx=10, pady=10)
        
        # Buttons Row 2
        tk.Button(btn_frame, text="View Summary", font=("Helvetica", 12), width=18, command=self.show_summary).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Highest Value", font=("Helvetica", 12), width=18, command=self.highest_value).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(btn_frame, text="Category Summary", font=("Helvetica", 12), width=18, command=self.category_summary).grid(row=1, column=2, padx=10, pady=10)
        
        # Buttons Row 3
        tk.Button(btn_frame, text="Monthly Chart", font=("Helvetica", 12), width=18, command=self.show_monthly_chart).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(btn_frame, text="Settings", font=("Helvetica", 12), width=18, command=self.settings_menu).grid(row=2, column=1, padx=10, pady=10)
        
        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)

    def update_balance(self):
        self.balance_label.config(text=f"Current Balance: ${self.money}")

    def add_expense(self):
        category = simpledialog.askstring("Expense", "Enter expense category:", parent=self.root)
        if category:
            amount_str = simpledialog.askstring("Expense", "Enter expense amount:", parent=self.root)
            if amount_str:
                try:
                    amount = int(amount_str)
                    if amount < 0: raise ValueError
                    self.money -= amount
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    self.history.append(["expense", category, amount, self.money, date_str])
                    self.save_data()
                    self.update_balance()
                    messagebox.showinfo("Success", "Expense added successfully!")
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid positive number.")

    def add_income(self):
        source = simpledialog.askstring("Income", "Enter income source:", parent=self.root)
        if source:
            amount_str = simpledialog.askstring("Income", "Enter income amount:", parent=self.root)
            if amount_str:
                try:
                    amount = int(amount_str)
                    if amount < 0: raise ValueError
                    self.money += amount
                    date_str = datetime.now().strftime("%Y-%m-%d")
                    self.history.append(["income", source, amount, self.money, date_str])
                    self.save_data()
                    self.update_balance()
                    messagebox.showinfo("Success", "Income added successfully!")
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid positive number.")
                    
    def show_history(self):
        hist_win = tk.Toplevel(self.root)
        hist_win.title("Transaction History")
        hist_win.geometry("700x450")
        
        tk.Label(hist_win, text="Select a record to Edit or Delete", font=("Helvetica", 10)).pack(pady=5)
        
        tree_frame = tk.Frame(hist_win)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Date", "Type", "Category", "Amount", "Balance"), show="headings", yscrollcommand=scrollbar.set)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Category", text="Category/Source")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Balance", text="Balance After")
        
        self.tree.column("ID", width=40, anchor=tk.CENTER)
        self.tree.column("Date", width=90, anchor=tk.CENTER)
        self.tree.column("Type", width=70)
        self.tree.column("Category", width=140)
        self.tree.column("Amount", width=90, anchor=tk.E)
        self.tree.column("Balance", width=90, anchor=tk.E)
        
        self.refresh_tree()
            
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        btn_frame = tk.Frame(hist_win)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Edit Selected", command=self.edit_record).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_record).pack(side=tk.LEFT, padx=5)

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, item in enumerate(self.history):
            date_str = item[4] if len(item) > 4 else "Unknown"
            self.tree.insert("", tk.END, iid=str(i), values=(i+1, date_str, item[0].capitalize(), item[1], f"${item[2]}", f"${item[3]}"))

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
        index = int(selected[0])
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            del self.history[index]
            self.save_data()
            self.refresh_tree()
            messagebox.showinfo("Success", "Record deleted.")

    def edit_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return
        index = int(selected[0])
        
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Record")
        edit_win.geometry("300x200")
        
        tk.Label(edit_win, text="Edit the transaction:", font=("Helvetica", 12)).pack(pady=10)
        
        def edit_cat():
            new_cat = simpledialog.askstring("Edit", "Enter new category:", parent=edit_win, initialvalue=self.history[index][1])
            if new_cat:
                self.history[index][1] = new_cat
                self.save_data()
                self.refresh_tree()
                messagebox.showinfo("Success", "Category updated.")
        
        def edit_amt():
            new_amt = simpledialog.askstring("Edit", "Enter new amount:", parent=edit_win, initialvalue=str(self.history[index][2]))
            if new_amt:
                try:
                    self.history[index][2] = int(new_amt)
                    self.save_data()
                    self.refresh_tree()
                    messagebox.showinfo("Success", "Amount updated.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount.")
                    
        tk.Button(edit_win, text="Edit Category", command=edit_cat, width=20).pack(pady=5)
        tk.Button(edit_win, text="Edit Amount", command=edit_amt, width=20).pack(pady=5)
        tk.Button(edit_win, text="Done", command=edit_win.destroy, width=20).pack(pady=5)
        
    def show_summary(self):
        summary_win = tk.Toplevel(self.root)
        summary_win.title("Summary")
        summary_win.geometry("300x250")
        summary_win.configure(padx=20, pady=20)
        
        total_expenses = sum(item[2] for item in self.history if item[0] == "expense")
        total_income = sum(item[2] for item in self.history if item[0] == "income")
        
        tk.Label(summary_win, text="Summary", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        tk.Label(summary_win, text=f"Total Transactions: {len(self.history)}", font=("Helvetica", 12)).pack(anchor=tk.W, pady=5)
        tk.Label(summary_win, text=f"Total Income: ${total_income}", font=("Helvetica", 12), fg="green").pack(anchor=tk.W, pady=5)
        tk.Label(summary_win, text=f"Total Expenses: ${total_expenses}", font=("Helvetica", 12), fg="red").pack(anchor=tk.W, pady=5)
        tk.Label(summary_win, text=f"Net Balance: ${self.money}", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=15)

    def highest_value(self):
        highest_exp = 0
        cat_exp = ""
        highest_inc = 0
        cat_inc = ""
        for item in self.history:
            if item[0] == "expense" and item[2] > highest_exp:
                highest_exp, cat_exp = item[2], item[1]
            elif item[0] == "income" and item[2] > highest_inc:
                highest_inc, cat_inc = item[2], item[1]
                
        msg = (f"Highest Expense: ${highest_exp}\n"
               f"Category: {cat_exp}\n\n"
               f"Highest Income: ${highest_inc}\n"
               f"Category: {cat_inc}")
        messagebox.showinfo("Highest Value", msg)
        
    def category_summary(self):
        cat_exp = {}
        cat_inc = {}
        for item in self.history:
            if item[0] == "expense":
                cat_exp[item[1]] = cat_exp.get(item[1], 0) + item[2]
            elif item[0] == "income":
                cat_inc[item[1]] = cat_inc.get(item[1], 0) + item[2]
                
        win = tk.Toplevel(self.root)
        win.title("Category Summary")
        win.geometry("400x400")
        
        tk.Label(win, text="Category-wise Expenses", font=("Helvetica", 14, "bold")).pack(pady=5)
        for cat, amt in cat_exp.items():
            tk.Label(win, text=f"{cat}: ${amt}").pack()
            
        tk.Label(win, text="Category-wise Income", font=("Helvetica", 14, "bold")).pack(pady=(15,5))
        for cat, amt in cat_inc.items():
            tk.Label(win, text=f"{cat}: ${amt}").pack()

    def show_monthly_chart(self):
        monthly_totals = {}
        for item in self.history:
            if item[0] == "expense":
                date_str = item[4] if len(item) > 4 else "Unknown"
                if date_str != "Unknown":
                    month = date_str[:7]
                else:
                    month = "Unknown"
                monthly_totals[month] = monthly_totals.get(month, 0) + item[2]
                
        chart_win = tk.Toplevel(self.root)
        chart_win.title("Monthly Expense Chart")
        chart_win.geometry("600x400")
        
        if not monthly_totals:
            tk.Label(chart_win, text="No expense data available.", font=("Helvetica", 14)).pack(pady=50)
            return
            
        tk.Label(chart_win, text="Monthly Expenses", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        canvas = tk.Canvas(chart_win, width=550, height=300, bg="white")
        canvas.pack(pady=10)
        
        max_val = max(monthly_totals.values())
        max_val = max_val if max_val > 0 else 1
        
        # Dimensions
        c_width = 550
        c_height = 250
        padding = 40
        
        # Axes
        canvas.create_line(padding, padding, padding, c_height, width=2)
        canvas.create_line(padding, c_height, c_width - padding, c_height, width=2)
        
        months = sorted(list(monthly_totals.keys()))
        num_bars = len(months)
        bar_width = min((c_width - 2 * padding) / (num_bars + 1), 80)
        
        for i, month in enumerate(months):
            total = monthly_totals[month]
            bar_height = (total / max_val) * (c_height - 2 * padding)
            
            x0 = padding + (i + 1) * ((c_width - 2 * padding) / (num_bars + 1)) - bar_width/2
            y0 = c_height - bar_height
            x1 = x0 + bar_width
            y1 = c_height
            
            canvas.create_rectangle(x0, y0, x1, y1, fill="#ff6b6b")
            canvas.create_text((x0 + x1)/2, y1 + 15, text=month, font=("Helvetica", 8))
            canvas.create_text((x0 + x1)/2, y0 - 10, text=f"${total}", font=("Helvetica", 8))

    def settings_menu(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("300x300")
        win.configure(padx=20, pady=20)
        
        tk.Label(win, text="Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 10))
        
        tk.Button(win, text="About", width=20, command=self.about).pack(pady=10)
        tk.Button(win, text="Reset Money", width=20, command=self.reset_money).pack(pady=10)
        tk.Button(win, text="Reset History", width=20, command=self.reset_history).pack(pady=10)
        tk.Button(win, text="Close", width=20, command=win.destroy).pack(pady=10)
        
    def about(self):
        msg = (
            "===================================\n"
            "      Braince Expense v1.8 (UI)\n"
            "===================================\n"
            "Creator : Prakhar Verma\n"
            "Organization : Braincells\n"
            "Version : v1.8\n"
            "Language : Python (Tkinter)\n\n"
            "A simple expense tracker\n"
            "to manage income, expenses\n"
            "and personal budgets.\n\n"
            "Upgraded from terminal to desktop GUI."
        )
        messagebox.showinfo("About", msg)
        
    def reset_money(self):
        if messagebox.askyesno("Reset Money", "Are you sure you want to reset the money? (History will be kept)"):
            new_budget_str = simpledialog.askstring("New Budget", "Enter your new budget:", parent=self.root)
            if new_budget_str:
                try:
                    self.money = int(new_budget_str)
                    self.save_data()
                    self.update_balance()
                    messagebox.showinfo("Success", "Money reset successfully!")
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount.")
                    
    def reset_history(self):
        if messagebox.askyesno("Reset History", "Are you sure you want to reset the history? (Balance will be kept)"):
            self.history.clear()
            self.save_data()
            messagebox.showinfo("Success", "History cleared!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerUI(root)
    root.mainloop()