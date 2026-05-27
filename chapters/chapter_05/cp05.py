# ch05.py — if Statements
# ---------------------------------------------------------
# Базовые ветвления, проверки списков и множественные условия

# 1. if-elif-else и числовые/строковые сравнения
alien_color = 'green'

if alien_color == 'green':
    print("You earned 5 points!")
elif alien_color == 'yellow':
    print("You earned 10 points!")
else:
    print("You earned 15 points!")

# 2. Проверка наличия/отсутствия элемента в списке (in / not in)
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'

if user not in banned_users:
    print(f"{user.title()}, you can post a response.")

# 3. Множественные независимые проверки (когда нужно проверить ВСЁ)
requested_toppings = ['mushrooms', 'extra cheese']

if 'mushrooms' in requested_toppings:
    print("Adding mushrooms.")
if 'pepperoni' in requested_toppings:
    print("Adding pepperoni.")
if 'extra cheese' in requested_toppings:
    print("Adding extra cheese.")

# 4. Проверка на пустоту списка (PEP 8)
empty_list = []
if empty_list: # Вернет False, так как список пуст
    print("List has items")
else:
    print("List is empty")