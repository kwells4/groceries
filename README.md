# Grocery list creator

This script and ajoining text file can be used to create a grocery list. It takes an input of meals and other ingredients, finds any common ingredients, and returns a list with the amount of each ingredient needed for the shopping trip.

## Adding meals
To add a new meal, open the `ingredients.txt` file. New meals must have the following format:

```
Name:
Meal_name1

Main Ingredients:
Ingredient_1: 1
Ingredient_2: 3

Other Ingredients:
Ingredient_3: 2
Ingredient_4: 1

Name:
Meal_name2

Main Ingredients:
Ingredient_6: 1
Ingredient_2: 3

Other Ingredients:
Ingredient_7: 6
Ingredient_4: 1
```

A few things to note

1. There must be a single empty line between each of the catgories
2. `Name:`, `Main Ingredients:`, and `Other_Ingredients:` must always be present exactly as shown
3. I use the main ingredients for things I will always need to buy - fruits and vegetables, tortillas, other ingredients contains things like flour that I should make sure I have but I might not need to buy every week.
4. The amount of the ingredient always must come after a colon and a space `: `

## Running the program
To run the program

```bash
python groceries.py
```

It will ask for a list of meals. These are the same names that are under the "Name" sections in the ingredients file. If you want to know what is available, typing "options" will print out a list of meal names that are alphabetically sorted.

To add meals, just type the meal names as a comma separated list. If you want to double a meal (like you are making it for a group) you can do this in two ways:
1. Type the meal name twice `Tomato soup, Vegetarian pot pie, Tomato soup`
2. Add a colon with the number of times you want `Tomato soup: 5, Vegetarian pot pie`

I have also added in some specific language to take any meals with `pizza` in the name and provide the user an option to just say `Pizza` first and then be promted what types of pizza are desired for the shopping trip.

The user will also be promted to write other items to add to the list. These can be added as a comma separated list or using the colon as described above to indeicate more than 1 (ie `Apples: 10`)

If the user supplies a meal that is not in the `ingredients.txt` file, the program will exit with an error message the prints what meals were not recoginized.