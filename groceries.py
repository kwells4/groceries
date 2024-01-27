from collections import defaultdict
import weakref
from collections import Counter
import re
import sys

def main():
	# Path to all meals
	meal_path = "ingredients.txt"
	meals = []
	units_path = "units.txt"
	units = {}

	read_units(units_path, units)

	read_meals(meal_path, meals)

	meal_list = []

	for obj in Meal.getinstances():
		meal_list.append(obj.name) 

	# Pull out pizza meals, if the user supplies "pizza", then prompt to ask
	# what kind of pizza
	pizza_meals = [meal.name for meal in meals if 'pizza' in meal.name]

	# Remove those meals and just put "pizza" for the meal names displayed to the user
	not_pizza_meals = [meal.name for meal in meals if "pizza" not in meal.name]
	not_pizza_meals.append("Pizza")

	user_meals = get_user_meals(pizza_meals, not_pizza_meals)

	other_ingredients = get_other_food()


	new_dict = fix_meal_names(user_meals)

	# Check if meals are present
	check_meals(new_dict, meal_list)


	user_main_ingredients = defaultdict(int)
	user_other_ingredients = defaultdict(int)

	generate_list(new_dict, user_main_ingredients, user_other_ingredients, other_ingredients)

	print_list(user_main_ingredients, user_other_ingredients, units)

################
# Read in data #
################

def read_units(units_path, units):
	# Read in units
	with open(units_path, "r") as units_file:
		for line in units_file:
			ingredient, unit = line.strip().split(": ")
			units[ingredient] = unit

def read_meals(meal_path, meals):
	# Read in meals
	with open(meal_path, "r") as meal_file:
		new_meal = False
		ingredients = False
		other_ingredients = False
		for line in meal_file:

			# Make a new meal instance
			if line.strip() == "Name:":
				new_meal = True
				ingredients = False
				other_ingredients = False
				name = next(meal_file).strip().capitalize()

				main_ingredients_dict = {}
				other_ingredients_dict = {}
				ingredients_dict = {}

			# Add main ingredients
			elif line.strip() == "Main Ingredients:":
				ingredients = True
				new_meal = False
				other_ingredients = False

			# Add other ingredients
			elif line.strip() == "Other Ingredients:":
				ingredients = False
				other_ingredients = True
				new_meal = False	

			# Add to dictionary of ingredients		
			elif ingredients and line.strip() == "":
				ingredients_dict["Ingredients"] = main_ingredients_dict
			elif ingredients:
				item, ammount = line.strip().split(": ")
				main_ingredients_dict[item] = float(ammount)

			# Generate a meal instance
			elif other_ingredients and line.strip() == "":
				ingredients_dict["other_ingredients"] = other_ingredients_dict
				new_meal = Meal(name, main_ingredients_dict, other_ingredients_dict)
				meals.append(new_meal)
			elif other_ingredients:
				item, ammount = line.strip().split(": ")
				other_ingredients_dict[item] = float(ammount)

	# Generate the final meal
	new_meal = Meal(name, main_ingredients_dict, other_ingredients_dict)

	# Add the final meal to the list
	meals.append(new_meal)

#######################
# Get input from user #
#######################

def get_user_meals(pizza_meals, not_pizza_meals):
	# Get list of meals from user:
	user_meals = input("Enter meals separated by a comma to see all options, type 'options': ") 
	if user_meals == "options" or user_meals == "Options":
		print(sorted(not_pizza_meals))
		user_meals = input("Enter meals separated by a comma: ")

	user_meals = user_meals.split(", ")

	# Check for pizza, remove and replace with the correct type of pizza
	if "Pizza" in user_meals or "pizza" in user_meals:
	    user_meals.remove("Pizza")

	    # Pull out new meals
	    pizza_types = input("What type of pizza would you like? Enter names separated by a comma. \n\
	    	To see all options type 'options': ")

	    if pizza_types == "options" or pizza_types == "Options":
	        print(sorted(pizza_meals))
	        pizza_types = input("Enter pizza names separated by a comma: ")

	    pizza_types = pizza_types.split(", ")

	    # Add pizza meals to the full list
	    user_meals.extend(pizza_types)

	# Count if any meal was added more than once
	user_meals = Counter(user_meals)

	return user_meals


def get_other_food():
	# Get list of other food from user
	other_food = input("Enter other food to add to list (like Milk, breakfast fruit): ")

	other_food = other_food.split(", ")

	return other_food

#######################
# Fix and check names #
#######################
def fix_meal_names(user_meals):
	# Check if any meal is used twice, here that will look like meal: 2
	new_dict = {}
	for i in user_meals.keys():
		if ":" in i:
			new_name = re.sub(":.*", "", i)
			new_val = re.sub(".*:", "", i)
			new_dict[new_name] = float(new_val)
		else:
			new_dict[i] = user_meals[i]

	# Capitalize the first letter to match case with the meals
	new_dict = {i.capitalize():k for (i,k) in new_dict.items()}

	return new_dict

def check_meals(new_dict, meal_list):
	# Check if any meals are not present in the list
	not_present = [i for i in new_dict.keys() if i not in meal_list]

	# If any meals aren't present, exit the program
	if len(not_present) >= 1:
		print("!!!!! Unknown meals !!!!!")
		for i in not_present:
			print(i + " is not in the known meal list")
		sys.exit()


#################
# Generate list #
#################

def generate_list(new_dict, user_main_ingredients, user_other_ingredients,
	other_food):
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

def print_list(user_main_ingredients, user_other_ingredients, units):
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

#########
# Class #
#########

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

if __name__ == "__main__":
	main()