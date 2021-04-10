class Category:

  def __init__(self, budgetCat):
    self.balance = 0
    self.name = budgetCat
    self.ledger = []
    print(self.name, "constructed")
  
  def check_funds(self, amount):
    if self.balance < amount:
      print('Insufficient funds.')
      return False
    else:
      return True

  def deposit(self, amount, description=""):
    self.ledger.append({"amount": amount, "description": description})
    self.balance = self.balance + amount
    return f"Deposited {amount} to {self.name}. New balance: {self.balance}"

  def withdraw(self, amount, description=""):
    if self.check_funds(amount) == False:
      return False
    else:
      self.ledger.append({"amount": -amount, "description": description})
      self.balance = self.balance - amount
      print(f"Withdrew {amount} from {self.name}. New balance: {self.balance}")
      return True

  def get_balance(self):
    return self.balance

  def transfer(self, amount, otherBudgetCat):
    originalCat = self.name
    if self.check_funds(amount) == False:
      return False
    else:
      self.ledger.append({"amount": -amount, "description": f"Transfer to {otherBudgetCat.name}"})
      self.balance = self.balance - amount
      print(f"Withdrew {amount} from {self.name}. New balance: {self.balance}")

      otherBudgetCat.ledger.append({"amount": amount, "description": f"Transfer from {originalCat}"})
      otherBudgetCat.balance = otherBudgetCat.balance + amount
      print(f"Deposited {amount} to {self.name}. New balance: {self.balance}")
      return True

  def __str__(self):
    astAmount = (30 - len(self.name))//2
    titleLine = astAmount*"*" + self.name + astAmount*"*" + "\n"
    transLines = ""
    for i in range(len(self.ledger)):
      space = (30 - (len(self.ledger[i]["description"][:23]) + len(str("%.2f" % self.ledger[i]["amount"]))))*" "
      newLine = self.ledger[i]["description"][:23] + space + str("%.2f" % self.ledger[i]["amount"]) + "\n"
      transLines += newLine
    totalLine = "Total: " + str("%.2f" % self.balance)

    return titleLine + transLines + totalLine

def create_spend_chart(categories):
  totalSpent = 0
  catSpending = {}
  # iterate through the categories ["Clothing", "Groceries", "Entertainment", "Food"]
  for i in range(len(categories)):
    # create category key in catSpending dictionary and set value to 0
    catSpending[categories[i].name] = 0
    # iterate through each entry in the ledger of the category
    for j in range(len(categories[i].ledger)):
      # if entry is a withdrawal(negative)
      if categories[i].ledger[j]["amount"] < 0:
        # add that amount to the value of the category key
        catSpending[categories[i].name] += abs(int(categories[i].ledger[j]["amount"]))
        totalSpent += abs(int(categories[i].ledger[j]["amount"]))
  
  # get percentage of each category
  percentages = []
  def round_down(num, divisor):
    return num - (num%divisor)
  for k,v in catSpending.items():
    perc = round_down((v / totalSpent)*100, 10)
    percentages.append(perc)
  
  titleLine2 = "Percentage spent by category\n"

  horizontalLine = "    " + ((len(categories)*3)+1)*"-" + "\n"

  percCalc = 100
  percLines = ''
  while percCalc >= 0:
    percLine = ''
    pos1 = ''
    pos2 = ''
    pos3 = ''
    pos4 = ''
    try:
      if percentages[0] >= percCalc:
        pos1 = " o "
      else:
        pos1 = "   "
    except:
      pos1 = "   "
      
    try:
      if percentages[1] >= percCalc:
        pos2 = " o "
      else:
        pos2 = "   "
    except:
      pos2 = "   "
    
    try:
      if percentages[2] >= percCalc:
        pos3 = " o "
      else:
        pos3 = "   "
    except:
      pos3 = "   "

    try:   
      if percentages[3] >= percCalc:
        pos4 = " o "
      else:
        pos4 = "   "
    except:
      pos4 = " "

    if percCalc == 100:
      percLine = str(percCalc) + "|" + pos1 + pos2 + pos3 + pos4
    elif percCalc == 0:
      percLine = "  " + str(percCalc) + "|" + pos1 + pos2 + pos3 + pos4
    else:
      percLine = " " + str(percCalc) + "|" + pos1 + pos2 + pos3 + pos4

    
    percCalc -= 10
    percLines += percLine + "\n"

  catLetters = []
  longestCatLen = -1
  for i in range(len(categories)):
    catLetter = []
    for j in range(len(str(categories[i].name))):
      catLetter.append(categories[i].name[j])
      if len(str(categories[i].name)) > longestCatLen:
        longestCatLen = len(str(categories[i].name))
    catLetters.append(catLetter)
  catNameLines = ''
  for i in range(longestCatLen):
    catNameLine = ''
    pos1 = ''
    pos2 = ''
    pos3 = ''
    pos4 = ''
    try:
      pos1 = f" {catLetters[0][i]} "
    except:
      pos1 = "   "
      
    try:
      pos2 = f" {catLetters[1][i]} "
    except:
      pos2 = "   "
    
    try:
      pos3 = f" {catLetters[2][i]} "
    except:
      pos3 = "   "

    try:   
      pos4 = f" {catLetters[3][i]} "
    except:
      pos4 = " "

    catNameLine = "    " + pos1 + pos2 + pos3 + pos4

    if i == longestCatLen - 1:
      catNameLines += catNameLine
    else:
      catNameLines += catNameLine + "\n"

  barChart = f'{titleLine2}{percLines}{horizontalLine}{catNameLines}'

  return barChart