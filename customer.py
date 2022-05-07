from faker import Faker
import random
import numpy as np
#import time
import pandas as pd

# The Auto increment function for Customer ID
def increment():
    """auto-increment by 1 starting from 1 (for customer_no)"""
    i = 1
    while True:
        yield i
        i = i + 1

AUTO_INCREMENT = increment() 
STATES= ['checkout','dairy','drinks','fruit','spices']  # Possible states
FAKE = Faker() # Faker object initiation
TRANS_MATRIX=pd.read_csv("data/trans_matrix.csv", index_col=0) # Reading Trans_Matrix file

class Customer:
    
    def __init__(self, budget=100):
        """the constructor of Customer Class

        Args:
            budget (int, optional): Customer Budget. Defaults to 100.
        """
        self.current_location = np.random.choice(
            ["dairy", "spices", "drinks", "fruit"]
            #p=first_probabilities["customer_id"].values,
        )
        new_customer_nr = next(AUTO_INCREMENT)
        self.customer_nr = new_customer_nr
        self.customer_name = FAKE.first_name()+" "+FAKE.last_name()
        self.budget=budget
        self.left="NO"
        #self.transition_probs=transition_probs

    def next_state(self):
        """allow a customer to go to the next state when the current location is not "checkout"

        Returns:
            NONE
        """
        if self.current_location != "checkout":
            self.current_location = self.random_next_state(TRANS_MATRIX,self.current_location,STATES)
        else:
            self.left="Ready"
            
        return self.current_location
    def is_active(self):
        """check a customer is active or not

        Returns:
            bool: the status of customer is active or not 
        """
        is_active_value=True
        if((self.current_location=="checkout")):
            is_active_value=False
            
        return is_active_value
        
    def __repr__(self):
        """definition of a customer

        Returns:
            string: the string presentation of a customer 
        """
        return f"""(id_{self.customer_nr}) is in section '{self.current_location}'."""
    
    def random_next_state(self,trans_matrix, current_state, states):
        """_summary_

        Args:
            trans_matrix (dataframe): transition matrix for next state calculation
            current_state (string): current state of a customer
            states (list): list of possible states

        Returns:
            string: next state of a customer
        """
        return random.choices(states, weights=trans_matrix.loc[current_state,:])[0]