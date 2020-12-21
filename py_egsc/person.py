from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Person():                                                #generic employee class
    def __init__(self,name):                                   #constructor
        self.name = name                                       #name
        self.person_id = None                                  #unique identifier
        self.payperiods = {}                                   #payperiod objects
        return
    
    def get_name(self):                                        #return name of person
        return(self.name)
    
    def get_payperiods(self):
        return(self.payperiods)
    
    def get_payperiod(self,school_year,seqno):
        try:
            return(self.payperiods[school_year][seqno])
        except IndexError:
            return({})
            
    def add_payperiod_by_index(self,syear,syseq,pperiod):        #payperiod school year and seqno
        if syear not in self.payperiods.keys():
            self.payperiods[syear] = {}
        if syseq not in self.payperiods[syear].keys():
            self.payperiods[syear][syseq] = pperiod
        return