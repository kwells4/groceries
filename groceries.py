from collections import defaultdict
import weakref
from collections import Counter
import re


import weakref

# Path to all meals
meal_path = "ingredients.txt"
meals = []
units_path = "units.txt"
units = {}

# Read in units
with open(units_path, "r") as units_file:
	for line in units_file:
		ingredient, unit = line.strip().split(": ")
		units[ingredient] = unit

# All meals

# Make an object for each meal
class Meal:
	_instances = set()
	def __init__(self, name, main_ingredients, other_ingredients):
		self.name = name
		self.ingredients = main_ingredients
		self.other_ingredients = other_ingredients
		self._instances.add(weakref.ref(self))
	@classmethod
	def getinstances(cls):
		dead = set()
		for ref in cls._instances:
			obj = ref()
			if obj is not None:
				yield obj
			else:
				dead.add(ref)
		cls._instances -= dead

# Read in meals
with open(meal_path, "r") as meal_file:
	new_meal = False
	ingredients = False
	other_ingredients = False
	for line in meal_file:
		if line.strip() == "Name:":
			new_meal = True
			ingredients = False
			other_ingredients = False
			name = next(meal_file).strip().capitalize()
			main_ingredients_dict = {}
			other_ingredients_dict = {}
			ingredients_dict = {}
		elif line.strip() == "Main Ingredients:":
			ingredients = True
			new_meal = False
			other_ingredients = False
		elif line.strip() == "Other Ingredients:":
			ingredients = False
			other_ingredients = True
			new_meal = False			
		elif ingredients and line.strip() == "":
			ingredients_dict["Ingredients"] = main_ingredients_dict
		elif ingredients:
			item, ammount = line.strip().split(": ")
			main_ingredients_dict[item] = float(ammount)
		elif other_ingredients and line.strip() == "":
			ingredients_dict["other_ingredients"] = other_ingredients_dict
			new_meal = Meal(name, main_ingredients_dict, other_ingredients_dict)
			meals.append(new_meal)
		elif other_ingredients:
			item, ammount = line.strip().split(": ")
			other_ingredients_dict[item] = float(ammount)

new_meal = Meal(name, main_ingredients_dict, other_ingredients_dict)
meals.append(new_meal)

meal_list = []

for obj in Meal.getinstances():
	meal_list.append(obj.name) 

# Get list of meals from user:
user_meals = input("Enter meals separated by a comma to see all options, type 'options': ") 
if user_meals == "options" or user_meals == "Options":
	print(meal_list)
	user_meals = input("Enter meals separated by a comma: ")

other_food = input("Enter other food to add to list (like Milk, breakfast fruit): ")

other_food = other_food.split(", ")

user_meals = user_meals.split(", ")

user_meals = Counter(user_meals)

new_dict = {}
for i in user_meals.keys():
    if ":" in i:
        new_name = re.sub(":.*", "", i)
        new_val = re.sub(".*:", "", i)
        new_dict[new_name] = float(new_val)
    else:
        new_dict[i] = user_meals[i]

new_dict = {i.capitalize():k for (i,k) in new_dict.items()}

not_present = [i for i in new_dict.keys() if i not in meal_list]

if len(not_present) >= 1:
	print("!!!!! Unknown meals !!!!!")
	for i in not_present:
		print(i + " is not in the known meal list")
	print("")
	print("")

user_main_ingredients = defaultdict(int)
user_other_ingredients = defaultdict(int)

for obj in Meal.getinstances():
	if obj.name in new_dict.keys():
		for item in obj.ingredients:
			user_main_ingredients[item] += obj.ingredients[item]*new_dict[obj.name]
		for other_item in obj.other_ingredients:
			user_other_ingredients[other_item] += obj.other_ingredients[other_item]*new_dict[obj.name]

for obj in other_food:
	if ":" in obj:
		obj, ammount = obj.split(": ")
		user_main_ingredients[obj] += float(ammount)
	else:
		user_main_ingredients[obj] += 1

print("")
print("")

print("Main ingredients:")
for item in user_main_ingredients:
	if item in units:
		print(item, user_main_ingredients[item], units[item])
	else:
		print(item, user_main_ingredients[item])

print("")
print("")

print("Other ingredients (check that you have enough of these):")
for other_item in user_other_ingredients:
	if other_item in units:
		print(other_item, user_other_ingredients[other_item], units[other_item])
	else:
		print(other_item, user_other_ingredients[other_item])