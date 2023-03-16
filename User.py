class User:
    def __init__(self):
        self.counter = 0
        self.cars = 0
        self.manufacturers = 0
        self.categories = 0
        self.styles = 0
        self.fuel = 0
        self.transmission = 0

    def setFavCar(self, cars):
        self.cars = cars
    
    def setFavManufacturers(self, manufacturers):
        self.manufacturers = manufacturers
    
    def setCategories(self, categories):
        self.categories = categories
    
    def setStyles(self, styles):
        self.styles = styles
    
    def setFuelTypes(self, fuel):
        self.fuel = fuel
    
    def setTransmissionTypes(self, transmission):
        self.transmission = transmission

    def getFavCar(self):
        return self.cars
    
    def getFavManufacturers(self):
        return self.manufacturers  
    
    def getCategories(self):
        return self.categories 
    
    def getStyles(self):
        return self.styles
    
    def getFuelTypes(self):
        return self.fuel 
    
    def getTransmissionTypes(self):
        return self.transmission

    def getDataUser(self):
        print("Car is: ", self.cars)
        print("Manufacturer is: ", self.manufacturers)
        print("Category is: ", self.categories)
        print("Style is: ", self.styles)
        print("Fuel is: ", self.fuel)
        print("Transmission is: ", self.transmission)
    
    def getCounter(self):
        return self.counter

    def setCounter(self, value):
        self.counter = value 