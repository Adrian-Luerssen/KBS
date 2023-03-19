class DAO:
    columns = ["make", "model", "fuel_type", "hp", "transmission", "driven_wheels", "doors", "category",
               "size", "style", "highway_mpg", "city_mpg", "popularity", "year", "price"]

    def __init__(self, datapath):
        self.cars_test = None
        self.path = datapath

    def readData(self):
        import pandas as pd
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
        cars_test = cars_test.groupby(
            ["make", "model", "fuel_type", "hp", "transmission", "driven_wheels", "doors", "category", "size", "style",
             "highway_mpg", "city_mpg", "popularity", "price"])["year"].max()
        cars_test = cars_test.reset_index()
        cars_test = cars_test.groupby(
            ["make", "model", "fuel_type", "hp", "transmission", "driven_wheels", "doors", "category", "size", "style",
             "highway_mpg", "city_mpg", "popularity", "year"])["price"].max()
        # print(cars_test_clean[cars_test_clean["Transmission Type"] == "MANUAL"])
        cars_test_clean = cars_test.reset_index()
        # print(cars_test_clean[cars_test_clean["Make"] == "Maserati"]["Market Category"])
        self.cars_test = cars_test_clean
        # show all cars from 2017 that are automatic
        # print(cars_test_clean[cars_test_clean["Year"] == 2017])

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
        print(search_terms)
        for key, value in search_terms.items():
            print("filtering by", key, ":", value)
            if value.lower() != "any":
                if key == "year":
                    matching_cars = matching_cars[matching_cars[key] >= int(value)]
                    matching_cars.sort_values(by=[key], ascending=False, inplace=True)
                elif key == "price":
                    matching_cars = matching_cars[matching_cars[key] <= int(value)]
                    matching_cars.sort_values(by=[key], ascending=True, inplace=True)
                elif key == "price_min":
                    matching_cars = matching_cars[matching_cars["price"] >= int(value)]
                    matching_cars.sort_values(by=[key], ascending=True, inplace=True)
                elif key == "doors":
                    matching_cars = matching_cars[matching_cars[key] >= int(value)]
                elif key == "hp" or key == "highway_mpg" or key == "city_mpg" or key == "popularity":
                    if value == "high":
                        matching_cars.sort_values(by=[key], ascending=False, inplace=True)
                    elif value == "low":
                        matching_cars.sort_values(by=[key], ascending=True, inplace=True)
                    # matching_cars = matching_cars[matching_cars[key] >= int(value)]
                # elif key == "cylinders":
                # matching_cars = matching_cars[matching_cars[key] >= int(value)] if user wants efficiency logic shouldn't provide more cylinders
                else:
                    print(key, value)
                    matching_cars = matching_cars[
                        matching_cars[key].apply(lambda x: str(x).lower() in str(value).lower())]
                    # matching_cars = [
                            # matching_cars[key].apply(lambda x: str(x).lower() in value.split(","))]

                print("No matching cars found." if matching_cars.empty else ("Matching cars:", matching_cars))

        # for key, value in term.items():
        # if value.lower() != "any":
        # matching_cars = matching_cars[matching_cars[key].apply(lambda x: str(value).lower() in str(x).lower())]

        # print(matching_cars["make"].apply(lambda x: userInput.lower() in str(x).lower()))


dao = DAO("data/data.csv")
dao.readData()
# dao.search("Bugatti")


# print("Search term: ")
# userInput = input()
# userInput = input().split(',')
# print(userInput)

# TODO: accept ranges in all numeric input for search parameters
# TODO: make categories array of strings instead of one string

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
