import Recommendation as rec

import PreProcessing as pre


q = rec.questions()
q.askQuestions()


#print(pre.preProcessing("I want a car that is fsat and has a lot of horspower and is a sedan and is a mercedes benz and is a 2018 and is a 4 door and is a 4 cylindr"))


#import DAO as dao
#dao = dao.DAO("data/data.csv")
#dao.readData()
#print(dao.searchCarsByPriority({"make":"toyota","model":"any","year": "any", "price": "50000.0","price_min":"10000.0", "doors": "4", "city_mpg": "high", "popularity": "any", "hp": "low", "cylinders": "low", "fuel_type": "electric", "transmission": "any", "driven_wheels": "any", "size": "any", "style": "any","category":"crossover"}))
#print(dao.searchCarsByPriority({'price': '50000.0', 'price_min': '0', 'highway_mpg': 'high', 'category': 'crossover'}))