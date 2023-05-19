import requests
import streamlit as st
import config
import math

# Register to get an APP ID and key https://developer.edamam.com/
app_id = config.application_id
app_key = config.application_key


includeAppId = "24eb7873"
includeAppKey = "dd47c3b662cfa8c3131362bf4641bf87"
startPagination = "0"
endPagination = "10"

CuisineType_array = {"American", "British", "Caribbean", "Chinese", "French", "Italian", "Japanese", "Kosher",
                     "Mediterranean", "Mexican"}

# ask user to enter ingredient(s)
inputIngredient = input("Please enter one or more ingredients to search for: ")
# return invalid response if user enters nothing or only spaces
while inputIngredient == "" or inputIngredient.isspace():
    inputIngredient = input("Invalid Response. Please enter at least one or more ingredients. Try again: ")
# prints out choose ingredient/s
# print("You have chosen these ingredients: " + inputIngredient)

# ask user to enter cuisine preference
inputCuisineType = input("Please enter a cuisine type ")
#print("You have chosen: " + inputCuisineType)


print(f'You have searched for {inputCuisineType} recipes using {inputIngredient}')

with open('recipes.txt', 'w') as f:
    rangeURL = f"https://api.edamam.com/search?q={inputIngredient}&cuisineType={inputCuisineType}&{includeAppId}&{includeAppKey}&from={startPagination}&to={endPagination}"
    rangeR = requests.get(rangeURL)

    if rangeR.status_code == 200:
        print("----")
        print("Your request was successful")
    else:
        print("----")
        print("Error: " + str(rangeR))

    data = rangeR.json()

    rangeCount = int(math.ceil(data['count'] / 10))
    # print(rangeCount)

    print("----")
    print(f"{data['count']} recipes found")

    for i in range(1, rangeCount):
        print("----")
        endPagination = i * 10
        startPagination = endPagination - 10
        url = f"https://api.edamam.com/search?q={inputIngredient}&cuisineType={inputCuisineType}&{includeAppId}&{includeAppKey}&from={startPagination}&to={endPagination}"
        print(f"Showing recipe results from {startPagination} to {endPagination}")
        r = requests.get(url)

        data = r.json()
        results = data['hits']
        # count = data['count']
        more = data['more']

        for result in results:
            recipe = result['recipe']
            print("----")
            print(recipe['label'])
            print(recipe['url'])
            f.write('%s\n' % recipe['label'])
            f.write('%s\n' % recipe['url'])
        if not more:
            print("----")
            print("That's all the recipes!")
            break
        print("----")
        moreRecipes = input("Do you want ten more recipes? Yes/No ")
        if moreRecipes.capitalize() == "No":
            print("----")
            print("enjoy a delicious meal")
        if moreRecipes.capitalize() != "Yes":
            break
