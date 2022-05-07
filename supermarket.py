"""
Start with this to implement the supermarket simulator.
"""

import numpy as np
import pandas as pd
#import time
from customer import Customer
import random

class Supermarket:
    """manages multiple Customer instances that are currently in the market.
    """

    def __init__(self, totaltime=60):        
        # a list of Customer objects
        self.customers = []
        self.minutes = 0
        self.current_time = 0
        self.all_locations=[]


    def __repr__(self):
        
        return f'Supermarket("{self.customers}", "{self.current_time}")'

    def get_time(self):
        """current time in HH:MM format,
        """
        hour = self.minutes // 60 + 8
        minutes = self.minutes % 60
        return f'{str(hour).zfill(2)}:{str(minutes).zfill(2)}'
        
    def print_customers(self):
        """print all customers with the current time and id in CSV format.
        """
        self.current_time = self.get_time()
        print(f'{self.current_time}')
        for cust in self.customers:
            if(cust.left=="NO"):
                dic={"time":self.current_time,"minute":self.minutes,"customer_id":cust.customer_nr, "location":cust.current_location}
                self.all_locations.append(dic)
                print(f'{cust}')

    def next_minute(self):
        """propagates all customers to the next state.
        """
        self.minutes += 1
        for cust in self.customers:
            if(cust.is_active()):
                cust.next_state()
            else:
                cust.left="Ready"
         
    def add_new_customers(self):
        """randomly creates new customers.
        """
        how_many=random.randint(0, 3)
        for i in range(how_many):
            cust=Customer()
            self.customers.append(cust)
        
    def remove_exitsting_customers(self):
        """removes every customer that is not active any more.
        """
        for cust in self.customers:
            if ((cust.is_active()==False) and (cust.left=="Ready")):
                print(f"{cust.customer_name} (id_{cust.customer_nr}) left")
                self.customers.remove(cust)
    
    def write_all_locations_to_csv(self):
        """add list of dictionary to data frame then csv file
        """             
        df = pd.DataFrame.from_dict(self.all_locations, orient='columns')
        df.to_csv("data/all_locations4.csv")
    
    
   
            
        
        