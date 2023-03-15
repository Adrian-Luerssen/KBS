class DAO:

    def __init__(self, datapath):
        self.path = datapath
        self.cars = {}
        self.manufacturers = {}
        self.categories = {}
        self.styles = {}
        self.fuelTypes = {}
        self.transmissionTypes = {}

    def readData(self):
        # Make	Model	Year	Engine Fuel Type	Engine HP	Engine Cylinders	Transmission Type	Driven_Wheels	Number of Doors	Market Category	Vehicle Size	Vehicle Style	highway MPG	city mpg	Popularity	MSRP

        cars = []
        with open(self.path) as file:
            line = file.readline()
            while True:
                line = file.readline()

                # print("line: "+ line)
                if not line:
                    break

                #remove \n
                line = line[:-1]
                split = line.split(",")
                for i in range(len(split)):
                    split[i] = split[i].lower()
                #turn split 9 into a list
                split[9] = split[9].split(";")
                ##all to lower case

                carString = split[0] + " " + split[1] + " " + split[11]
                if carString not in self.cars:
                    self.cars[carString] = split
                else:
                    # keep the newest car
                    if int(self.cars[carString][2]) < int(split[2]):
                        self.cars[carString] = split


                if split[0] not in self.manufacturers:
                    self.manufacturers[split[0]] = {}

                if split[1] not in self.manufacturers[split[0]]:
                    self.manufacturers[split[0]][split[1]] = []
                if split[11] not in self.manufacturers[split[0]][split[1]]:
                    self.manufacturers[split[0]][split[1]].append(split[11])

                for cat in split[9]:
                    if cat not in self.categories:
                        self.categories[cat] = []
                    self.categories[cat].append(carString)





                if split[11] not in self.styles:
                    self.styles[split[11]] = []
                self.styles[split[11]].append(carString)
                if split[3] not in self.fuelTypes:
                    self.fuelTypes[split[3]] = []
                self.fuelTypes[split[3]].append(carString)
                cars.append(line.split(","))
                if split[6] not in self.transmissionTypes:
                    self.transmissionTypes[split[6]] = []
                self.transmissionTypes[split[6]].append(carString)


        self.data = cars

    def search(self, make):
        make = make.lower()
        #print(self.manufacturers["BMW"]["1 Series M"])
        #print(self.cars)
        for model in self.manufacturers[make]:
            for style in self.manufacturers[make][model]:
                carString = make+" "+ model + " " + style
                print(carString + " : "+ str(self.cars[carString]))
            print()
        #print(self.cars["BMW 1 Series M Coupe"])
        #print(self.categories)
        #print(self.styles)
        #print(self.fuelTypes)


dao = DAO("data/data.csv")
dao.readData()
dao.search("Bugatti")
