import tkinter as tk
root = tk.Tk()
root.title("Braince Expense v1.8")
root.withdraw() # hide the tkinter root window

import json
from datetime import datetime

print("=" * 42)
print("        🧠 Braince Expense")
print("             v1.7")
print("=" * 42)
print("      Created by Prakhar Verma")
print("        Organization: Braincells")
print("=" * 42)
print(" Manage your money with simplicity")
print("=" * 42)
print()
money = int(input("enter your budget: "))
pin="1234"
p = input("enter pin: ")
if p == pin:
  function = True
else:
  print("oppsy wrong pin")
  print("1:try again")
  print("2:exit")
  ph=int(input("enter your choice:"))
  if ph == 1:
    p = input("enter pin: ")
    if p == pin:
      function = True
    else:
      function = False
history = []


def add_expenses():
  global money
  category = input("enter your expense category: ") 
  expense = int(input("enter your expenses: "))
  money = money-expense
  date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print("category:",category)
  print("remaing money",money)
  history.append(["expense",category,expense,money, date_str])

def add_income():
  global money
  source=input("income source:")
  income = int(input("enter your income/money: "))
  money = money + income
  date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print("balance",money)
  history.append(["income",source,income,money, date_str])

def show_balance():
  print("balance",money)

def show_history():
  nu = 1
  for item in history:
    print("===================================")
    date_str = item[4] if len(item) > 4 else "Unknown Date"
    print("type:", item[0])
    print("category:", item[1])
    print("Ammount:",item[2])
    print("Balance:",item[3])
    print("Date:", date_str)
    print("===================================")
  
def del_his():
  nu=1
  global history
    
  for item in history:
    print(nu,item)
    nu=nu+1
  de=int(input("enter transaction number"))
  del history[de-1]

def save_trex():
  file = open("expense.txt","w")
  file.write(str(money))
  file.close()

def edit_sys():
  nu=1
  global history
    
  for item in history:
    print(nu,item)
    nu=nu+1
  edit = int(input("enter transaction number:"))
  print("1:category")
  print("1:Ammount")
  co = int(input("enter your choice:"))
  if co==1:
    new_category = input("enter new category:")
    history [edit - 1] [1] = new_category
  if co==2:
    new_ammount = int(input("enter new ammount:"))
    history [edit - 1] [2] = new_ammount

def about():
  print("===================================")
  print("      Braince Expense v1.7")
  print("===================================")
  print("Creator : Prakhar Verma")
  print("Organization : Braincells")
  print("Version : v1.7")
  print("Language : Python")
  print("Platform : Terminal")
  print("")
  print("A simple expense tracker")
  print("to manage income, expenses")
  print("and personal budgets.")
  print("")
  print("upgraded from phone built to desktop version.")
  print("===================================")

def settings():
  print("====settings===")
  print("1:about")
  print("2:reset data")
  print("3:back")
  sh=int(input("enter your choice:"))
  if sh==1:
    about()
  if sh==2:
    print("1:reset money")
    print("2:reset history")
    rm = int(input("enter your choice: "))
    if rm==1:
      reset_money()
    if rm==2:
      reset_history()

def reset_money():
  global money
  print("are you sure u want to reset the money(Y/N)")
  rm=input("enter your choice:")
  if rm.upper() == "Y":
    money = int(input("enter your budget: "))
    print("money reset sucessfully")
  else:
    print("exiting")

def reset_history():
  global history
  print("are you sure u want to reset the history(Y/N)")
  rm=input("enter your choice:")
  if rm.upper() == "Y":
    history.clear()
    print("history cleared")
  else:
    print("exiting")

def summary():
  total_expenses = 0
  total_income = 0
  for item in history:
    if item[0] == "expense":
      total_expenses += item[2]
    elif item[0] == "income":
      total_income += item[2]
  print("Number of Transactions:", len(history))
  print("Total Expenses:", total_expenses)
  print("Total Income:", total_income)

def highest_value():
  highest_expense = 0
  category_expense = ""
  highest_income = 0
  category_income = ""
  for item in history:
    if item[0] == "expense" and item[2] > highest_expense:
      highest_expense = item[2]
      category_expense = item[1]
    elif item[0] == "income" and item[2] > highest_income:
      highest_income = item[2]
      category_income = item[1]
  print("Highest Expense:", highest_expense)
  print("Highest Income:", highest_income)
  print("Category of Highest Expense:", category_expense)
  print("Category of Highest Income:", category_income)

def category_summary():
  category_expenses = {}
  category_income = {}
  for item in history:
    if item[0] == "expense":
      if item[1] in category_expenses:
        category_expenses[item[1]] += item[2]
      else:
        category_expenses[item[1]] = item[2]
    elif item[0] == "income":
      if item[1] in category_income:
        category_income[item[1]] += item[2]
      else:
        category_income[item[1]] = item[2]
  print("Category-wise Expenses:")
  for category, amount in category_expenses.items():
    print(f"{category}: {amount}")
  print("Category-wise Income:")
  for category, amount in category_income.items():
    print(f"{category}: {amount}")

def monthly_chart():
  monthly_totals = {}
  for item in history:
    if item[0] == "expense":
      date_str = item[4] if len(item) > 4 else "Unknown"
      if date_str != "Unknown":
        month = date_str[:7]
      else:
        month = "Unknown"
      monthly_totals[month] = monthly_totals.get(month, 0) + item[2]
      
  print("\n--- Monthly Expense Chart ---")
  if not monthly_totals:
    print("No expense data available.")
    print("-----------------------------\n")
    return
    
  max_val = max(monthly_totals.values()) if monthly_totals else 1
  for month, total in sorted(monthly_totals.items()):
    bar_length = int((total / max_val) * 20)
    bar = "█" * bar_length
    print(f"{month:7} | ${total:<7} | {bar}")
  print("-----------------------------\n")

def save_data():
  data = {
    "money": money,
    "history": history
  }
  with open("data.json", "w") as file:
    json.dump(data, file)

def load_data():
  global money, history
  try:
    with open("data.json", "r") as file:
      data = json.load(file)
    money = data["money"]
    history = data["history"]
  except FileNotFoundError:
    money = 0
    history = []

load_data()

while function:
  print("1:add expense")
  print("2:add income")
  print("3:show balance")
  print("4:show history")
  print("5:delete record")
  print("6:edit history")
  print("7:settings")
  print("8:about")
  print("9:summary")
  print("10:highest value")
  print("11:category summary")
  print("12:monthly chart")
  choice = int(input("enter your choice: "))
  
  if choice == 1:
    add_expenses()
    save_data()
  
  if choice == 2:
    add_income()
    save_data()
  
  if choice == 3:
    show_balance()
  
  if choice == 4:
    show_history()
  
  if choice == 5:
    del_his()
    save_data()

  if choice==6:
    edit_sys()
    save_data()

  if choice==7:
    settings()
    save_data()
  
  if choice==9:
    summary()

  if choice==10:
    highest_value()

  if choice==11:
    category_summary()
    
  if choice==12:
    monthly_chart()

  ch= input("do you want to continue(Y/N)")
  if ch.upper() == "Y":
    print("continuing")
  
  else:
    function = False
    print("exiting") 
print("thank you for using Braince Expense v1.7")