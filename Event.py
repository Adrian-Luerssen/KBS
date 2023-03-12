"""
Created on Sun Mar 12 17:02:15 2023

@author: Sergi Vives
"""
class Event:
    events = []

    def __init__(self, name, day, month, time, length):
        self.name = name
        self.day = day
        self.month = month
        self.time = time
        self.length = length
    
    
