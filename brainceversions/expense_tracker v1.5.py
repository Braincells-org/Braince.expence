print("welcome to expense tracker v1.5")
history = []
money = int(input("enter your budget: "))

def add_expenses():
  global money
  category = input("enter your expense category: ") 
  expense = int(input("enter your expenses: "))
  money = money-expense
  print("category:",category)
  print("remaing money",money)

def add_income():
  global money
  source=input("income source:")
  income = int(input("enter your income/money: "))
  money = money + income
  print("balance",money)
  history.append(["income",source,income,money])

def show_balance():
  print("balance",money)

def show_history():
  nu = 1
  for item in history:
    print("===================================")
    print("type:", item[0])
    print("category:", item[1])
    print("Ammount:",item[2])
    print("Balance:",item[3])
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
  
function = True
while function:
  print("1:add expense")
  print("2:add income")
  print("3:show balance")
  print("4:show history")
  print("5:delete history")
  print("6:edit history")
  choice = int(input("enter your choice: "))
  
  if choice == 1:
    add_expenses()
    save_trex()
  
  if choice == 2:
    add_income()
  
  if choice == 3:
    show_balance()
  
  if choice == 4:
    show_history()
  
  if choice == 5:
    del_his()

  if choice==6:
    edit_sys()
  
  ch= input("do you want to continue(Y/N)")
  if ch.upper() == "Y":
    print("continuing")
  
  else:
    function = False
    print("exiting") 