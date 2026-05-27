# ch06.py — Dictionaries
# ---------------------------------------------------------
# Структуры ключ-значение (key-value), итерация и вложенность

# 1. Базовый словарь: создание, доступ, модификация
alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color']) # Доступ по ключу (выдаст KeyError если ключа нет)

alien_0['x_position'] = 0 # Добавление новой пары
alien_0['color'] = 'yellow' # Изменение существующей
del alien_0['points'] # Удаление пары ключ-значение

# Безопасный доступ через get() - не ломает код, если ключа нет
speed = alien_0.get('speed', 'No speed assigned')

# 2. Итерация (Перебор) словаря
user_0 = {'username': 'efermi', 'first': 'enrico', 'last': 'fermi'}

for key, value in user_0.items(): # Перебор пар
    print(f"Key: {key}, Value: {value}")

for key in user_0.keys(): # Перебор только ключей (поведение по умолчанию)
    print(key)

for value in set(user_0.values()): # Перебор только уникальных значений
    print(value)

# 3. Вложенность (Nesting): Список в словаре
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'], # Значение - это список
}
for topping in pizza['toppings']:
    print(f"Adding {topping} to your {pizza['crust']} pizza.")

# 4. Вложенность: Словарь в словаре (как JSON)
users = {
    'aeinstein': {'first': 'albert', 'last': 'einstein'},
    'mcurie': {'first': 'marie', 'last': 'curie'}
}
print(users['mcurie']['last']) # Доступ вглубь вложенности: curie