print("welcome to expense tracker v1.0")
money = 0
money = int(input("enter your budget: "))
function = True
while function:
  print("1:add expense")
  print("2:add income")
  print("3:show balance")
  choice = int(input("enter your choice: "))
  if choice == 1:
    category = input("enter your expense category: ") 
    expense = int(input("enter your expenses: "))
    money = money-expense
    print("category:",category)
    print("remaing money",money)
  if choice == 2:
    income = int(input("enter your income/money: "))
    money = money + income
    print("balance",money)
  if choice == 3:
    print("balance",money)
  ch= input("do you want to continue(Y/N)")
  if ch.upper() == "Y":
    print("continuing")
  else:
    function = False
    print("exiting")