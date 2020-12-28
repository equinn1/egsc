from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Scenario():                                              #scenario
    def __init__(self,sid,step,fte,payments,salary):           #constructor
        self.sid = sid                                         #identifier
        self.step = step                                       #step
        self.fte = fte                                         #fte
        self.payments = payments                               #payments
        self.salary = salary                                   #salary
        return
    
    def get_sid(self):                                         #return the identifier
        return(self.sid)
    
    def get_step(self):
        return(self.step)
    
    def get_fte(self):
        return(self.fte)
            
    def get_salary(self):
        return(self.salary)
            
    def get_payments(self):                          
        return(self.payments)