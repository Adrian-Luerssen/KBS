class DAO:

    def __init__(self, datapath):
        self.cars_test = None
        self.path = datapath

    def readData(self):
        import pandas as pd
        # Make	Model	Year	Fuel Type	HP	Cylinders	Transmission Type	Driven_Wheels	Number of Doors	Market Category	Vehicle Size	Vehicle Style	highway MPG	city mpg	Popularity	MSRP

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
            ["Make", "Model", "Fuel Type", "HP", "Transmission", "Driven_Wheels", "Doors", "Market Category", "Size",
             "Style", "highway MPG", "city MPG", "Popularity", "Price"])["Year"].max()
        cars_test = cars_test.reset_index()
        cars_test = cars_test.groupby(
            ["Make", "Model", "Fuel Type", "HP", "Transmission", "Driven_Wheels", "Doors", "Market Category", "Size",
             "Style", "highway MPG", "city MPG", "Popularity", "Year"])["Price"].max()
        # print(cars_test_clean[cars_test_clean["Transmission Type"] == "MANUAL"])
        cars_test_clean = cars_test.reset_index()
        print(cars_test_clean[cars_test_clean["Make"] == "Maserati"]["Model"])
        # show all cars from 2017 that are automatic
        # print(cars_test_clean[cars_test_clean["Year"] == 2017])
        # TODO: do dao.search()


    #declare a function called "search" which takes a string as a parameter and outputs all the cars that match the search term
    def search(self, searchTerm):
        print("searching for: ", searchTerm)
        print(self.cars_test[self.cars_test["Make"] == searchTerm])


dao = DAO("data/data.csv")
dao.readData()
# dao.search("Bugatti")

print("Search term: ")
userInput = input()
while userInput != "exit":
    # dao.search(userInput)
    print("Search term: ")
    userInput = input()
