import pandas as pd
import json
from datetime import datetime
pd.options.mode.chained_assignment = None
class DAO:
    columns = []

    def __init__(self, datapath):
        self.cars_test = None
        self.path = datapath
        self.readData()
    def readData(self):
        # make  model	year	fuel_type	hp	cylinders	transmission	driven_wheels	doors	category	size	style	highway_mpg	city_mpg	popularity	price

        pd.set_option('display.max_columns', 5000)
        pd.set_option('display.max_row', 100000)
        pd.max_columns = 1000
        cars_test = pd.read_csv(self.path)
        # print(cars_test[cars_test["Year"] == 2017])
        # print all cars from 2017 that are automatic
        # print(cars_test[(cars_test["Transmission Type"] == "AUTOMATIC") & (cars_test["Make"] == "Volvo") & (cars_test["Model"] == "V60")])
        # print(cars_test.describe())
        # print(cars_test.groupby(["Make", "Model", "Engine Fuel Type", "Transmission Type", ])["Year"].max())
        cars_test_clean = cars_test.groupby(
            ["make", "model", "fuel_type", "cylinders", "transmission", "doors", "category",
             "size", "style"])["year"].max()
        cars_test_clean = cars_test_clean.reset_index()
        cars_test_clean = pd.merge(cars_test_clean, cars_test[
            ["make", "model", "fuel_type", "cylinders", "transmission", "driven_wheels", "doors", "category",
             "size", "style", "price", "year"]],
                             on=["make", "model", "fuel_type", "cylinders", "transmission", "doors",
                                 "category", "size", "style","year"], how="left")
        cars_test_clean = cars_test_clean.groupby(
            ["make", "model", "fuel_type", "cylinders", "transmission", "doors", "category",
             "size", "style", "year"])["price"].max()
        cars_test_clean = cars_test_clean.reset_index()

        cars_test_clean = pd.merge(cars_test_clean, cars_test[
            ["make", "model", "fuel_type", "cylinders", "transmission", "driven_wheels", "doors", "category",
             "size", "style", "price", "year","hp","highway_mpg","city_mpg","popularity"]],
                                   on=["make", "model", "fuel_type", "cylinders", "transmission",
                                       "doors",
                                       "category", "size", "style", "year","price"], how="left")

        # print(cars_test_clean[cars_test_clean["Make"] == "Maserati"]["Market Category"])
        self.cars_test = cars_test
        columns = self.cars_test.columns
        # show all cars from 2017 that are automatic
        # print(cars_test_clean[cars_test_clean["Year"] == 2017])
        self.normalise()
        self.cars_test.columns = self.cars_test.columns.str.lower()



    def normalise(self):

        norm = pd.get_dummies(self.cars_test, columns=['fuel_type', 'transmission', 'driven_wheels', 'size', 'style'])
        categories = self.cars_test["category"].str.get_dummies(sep=";")

        # Rename the columns to include the "category_" prefix
        categories = categories.add_prefix("category_")

        # Concatenate the new columns to the original dataframe
        norm = pd.concat([norm, categories], axis=1)
        norm["fuel_type"] = self.cars_test["fuel_type"]
        norm["transmission"] = self.cars_test["transmission"]
        norm["driven_wheels"] = self.cars_test["driven_wheels"]
        norm["size"] = self.cars_test["size"]
        norm["style"] = self.cars_test["style"]
        #do a max min normalisation on the price, highway_mpg, city_mpg, popularity, year, hp, cylinders, doors
        norm["price_norm"] = (norm["price"] - norm["price"].min()) / (norm["price"].max() - norm["price"].min())
        norm["highway_mpg_norm"] = (norm["highway_mpg"] - norm["highway_mpg"].min()) / (norm["highway_mpg"].max() - norm["highway_mpg"].min())
        norm["city_mpg_norm"] = (norm["city_mpg"] - norm["city_mpg"].min()) / (norm["city_mpg"].max() - norm["city_mpg"].min())
        norm["popularity_norm"] = (norm["popularity"] - norm["popularity"].min()) / (norm["popularity"].max() - norm["popularity"].min())
        norm["year_norm"] = (norm["year"] - norm["year"].min()) / (norm["year"].max() - norm["year"].min())
        norm["hp_norm"] = (norm["hp"] - norm["hp"].min()) / (norm["hp"].max() - norm["hp"].min())
        norm["cylinders_norm"] = (norm["cylinders"] - norm["cylinders"].min()) / (norm["cylinders"].max() - norm["cylinders"].min())
        norm["doors_norm"] = (norm["doors"] - norm["doors"].min()) / (norm["doors"].max() - norm["doors"].min())
        #print(norm.head())
        self.cars_test = norm.reset_index()
        #print(self.cars_test.keys())

    def search(self, searchTerm):
        print("searching for: ", searchTerm)
        matching_cars = self.cars_test[
            self.cars_test.applymap(lambda x: searchTerm.lower() in str(x).lower()).any(axis=1)]
        if matching_cars.empty:
            print("No matching cars found.")
        else:
            print("Matching cars:")
            print(matching_cars)

    def searchParameters(self, *search_terms):
        print("searching for cars...")
        matching_cars = self.cars_test

        for i, term in enumerate(search_terms):
            if term.lower() != "any":
                matching_cars = matching_cars[
                    matching_cars[self.columns[i]].apply(lambda x: str(term).lower() in str(x).lower())]

        if matching_cars.empty:
            print("No matching cars found.")
        else:
            print("Matching cars:")
            print(matching_cars)

    def searchCarsByParameters(self, search_terms):
        print("searching for cars...")
        matching_cars = self.cars_test
        #print(search_terms)
        for key, value in search_terms.items():
            #print("filtering by", key, ":", value)
            if str(value).lower() != "any":
                if key == "year":
                    matching_cars = matching_cars[matching_cars[key] >= int(value)]
                    matching_cars.sort_values(by=key, ascending=False, inplace=True)
                elif key == "price":
                    matching_cars = matching_cars[matching_cars[key] <= int(value)]
                    matching_cars.sort_values(by="year", ascending=False, inplace=True)
                elif key == "price_min":
                    matching_cars = matching_cars[matching_cars["price"] >= int(value)]
                    matching_cars.sort_values(by="price", ascending=True, inplace=True)
                elif key == "doors":
                    matching_cars = matching_cars[matching_cars[key] >= int(value)]
                elif key == "hp" or key == "highway_mpg" or key == "city_mpg" or key == "popularity" or key == "cylinders":
                    if value == "high":
                        matching_cars.sort_values(by=key, ascending=False, inplace=True, na_position='last')
                    elif value == "low":
                        matching_cars.sort_values(by=key, ascending=True, inplace=True)
                elif key == 'mpg':
                    matching_cars.sort_values(by=["highway_mpg","city_mpg"], ascending=False, inplace=True)
                    # matching_cars = matching_cars[matching_cars[key] >= int(value)]
                # elif key == "cylinders":
                # matching_cars = matching_cars[matching_cars[key] >= int(value)] if user wants efficiency logic shouldn't provide more cylinders
                elif key == "category":
                    accepted = (value.lower()).split(",")
                    matching_cars = matching_cars[matching_cars[key].apply(lambda x: len(set(str(x).lower().split(";")).intersection(set(accepted))) > 0)]
                else:
                    print(key, value)
                    matching_cars = matching_cars[
                        matching_cars[key].apply(lambda x: str(x).lower() in str(value).lower())]
                    # matching_cars = [matching_cars[key].apply(lambda x: str(x).lower() in value.split(","))]
            #print("No matching cars found." if matching_cars.empty else ("Matching cars:", matching_cars.head(10)))

        # return cars as a list
        return matching_cars.head(10).values.tolist()

    def getWeight(self,search_terms):
        weight={}
        for key, value in search_terms.items():
            for val in value.split(","):
                #print("filtering by", key, ":", value)
                if key+"_norm" in self.cars_test.keys():
                    if str(val).lower() == "high":
                        weight[key+"_norm"] = 3
                    elif str(val).lower() == "any":
                        weight[key+"_norm"] = 1
                    elif str(val).lower() == "low":
                        weight[key+"_norm"] = 0.5
                #print(self.cars_test.keys())
                if key+"_"+str(val).lower() in self.cars_test.keys():
                    weight[key+"_"+str(val).lower()] = 3



        return weight
    def searchCarsByPriority(self,search_terms):
        #search based on priorities
        #calculate a score per car and return those with the highest score
        print("searching for cars...")
        matching_cars = self.cars_test.copy()
        normCols = []
        weights = self.getWeight(search_terms)
        #print(search_terms)
        for key, value in search_terms.items():
            #print(matching_cars.columns.tolist())
            #print("filtering by", key, ":", value)
            if (value.replace(".", "").isnumeric()):
                if key == "year" :
                    matching_cars = matching_cars[matching_cars[key] >= float(value)]
                elif key == "price":
                    matching_cars = matching_cars[matching_cars[key] <= float(value)]
                elif key == "price_min":
                    matching_cars = matching_cars[matching_cars["price"] >= float(value)]
                elif key == "doors":
                    matching_cars = matching_cars[matching_cars[key] == float(value)]
            elif str(value).lower() != "any":
                if key == "doors" or key == "city_mpg" or key == "popularity" or key == "hp" or key == "cylinders":
                    normCols.append(key+"_norm")
                    if (not((key+"_norm") in weights)):
                        weights[key+"_norm"] = 1
                elif key == "fuel_type" or key == "transmission" or key == "driven_wheels" or key == "size" or key == "style":
                    normCols.append(key+"_"+value.lower())
                    if (not(key+"_"+value.lower() in weights)):
                        weights[key+"_"+value.lower()] = 1



                    # matching_cars = [matching_cars[key].apply(lambda x: str(x).lower() in value.split(","))]
            # print("No matching cars found." if matching_cars.empty else ("Matching cars:", matching_cars.head(10)))
        scores = []
        #print(weights)
        for i, row in matching_cars.iterrows():
            score = sum(weights[key] * row[key] for key in weights.keys() if key in row.index)
            scores.append(score)
        #print(matching_cars)
        matching_cars["score"] = scores

        #print(matching_cars.columns.tolist())
        #group by make and model
        cars_test_clean = matching_cars.groupby(["make","model"])[["index","score"]].max()



        cars_test_clean = pd.merge(cars_test_clean, matching_cars[
            ["index","make", "model", "fuel_type", "cylinders", "transmission", "driven_wheels", "doors", "category",
             "size", "style", "price", "year", "hp", "highway_mpg", "city_mpg", "popularity", "score"]],
                                   on=["index"], how="inner")

        matching_cars = cars_test_clean
        #print(matching_cars.head(10))
        self.columns = matching_cars.columns.tolist()
        #print(self.columns)
        return matching_cars.sort_values(by="score_x", ascending=False).head(10).values.tolist()

    def showCarInfo(self,car):
        print("Showing car info...")
        car_data = self.cars_test.loc[self.cars_test["index"] == car]

        # Extract information from the DataFrame
        make = car_data["make"].values[0]
        model = car_data["model"].values[0]
        year = car_data["year"].values[0]
        hp = car_data["hp"].values[0]
        cylinders = car_data["cylinders"].values[0]
        doors = car_data["doors"].values[0]
        category = " ".join(car_data["category"].values[0].split(";"))
        highway_mpg = car_data["highway_mpg"].values[0]
        city_mpg = car_data["city_mpg"].values[0]
        popularity = car_data["popularity"].values[0]
        price = car_data["price"].values[0]
        fuel_type = car_data["fuel_type"].values[0]
        transmission = car_data["transmission"].values[0]
        driven_wheels = car_data["driven_wheels"].values[0]
        size = car_data["size"].values[0]
        style = car_data["style"].values[0]

        # Print the information in a nice format
        print(f"Make: {make}")
        print(f"Model: {model}")
        print(f"Year: {year}")
        print(f"Horsepower: {hp}")
        print(f"Cylinders: {cylinders}")
        print(f"Doors: {doors}")
        print(f"Category: {category}")
        print(f"Highway MPG: {highway_mpg}")
        print(f"City MPG: {city_mpg}")
        print(f"Popularity: {popularity}")
        print(f"Price: ${price}")
        print(f"Fuel Type: {fuel_type}")
        print(f"Transmission: {transmission}")
        print(f"Driven Wheels: {driven_wheels}")
        print(f"Size: {size}")
        print(f"Style: {style}")
    def saveCarInfo(self,car,filters):
        #save answer information to answers.json with timestamp
        with open('data/answers.json') as json_file:
            data = json.load(json_file)
            data.append({
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "filters": filters,
                "car": car
            })
        with open('data/answers.json', 'w') as outfile:
            json.dump(data, outfile)

    def dataAnalysis(self):
        import matplotlib.pyplot as plt
        import seaborn as sns
        import os
        data = self.cars_test.copy()
        data = data.drop(columns=["make","model","category","fuel_type","transmission","driven_wheels","size","style","index","price_norm","year_norm","hp_norm","highway_mpg_norm","city_mpg_norm","popularity_norm","doors_norm","cylinders_norm"])
        fig, axes = plt.subplots(1, 1, figsize=(50, 30))
        sns.heatmap(data.corr(), annot=True)
        fig.tight_layout()
        if not os.path.exists("data"):
            os.makedirs("data")
        plt.savefig("data/heatmap.png")

#dao = DAO("data/data.csv")
#dao.readData()
# dao.search("Bugatti")

# print("Search term: ")
# userInput = input()
# userInput = input().split(',')
# print(userInput)

# dao.searchCarsByParameters({"make": "porsche", "model": "any", "year": "1990", "price": "any", "city_mpg": "any", "size": "midsize,large"})

# dao.searchParameters(*[term.strip() for term in userInput])
# dao.search(userInput)
#while userInput != ["exit"]:
    # dao.search(userInput)
    #print("Search term: ")
    # userInput = input()
    # dao.search(userInput)
    #userInput = input().split(',')
    # dao.searchParameters(*[term.strip() for term in userInput])
