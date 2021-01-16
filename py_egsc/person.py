from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Person():                                                #generic employee class
    def __init__(self,name):                                   #constructor
        self.name = name                                       #name
        self.person_id = None                                  #unique identifier
        self.roles = {}                                        #roles
        return
    
    def get_name(self):                                        #return name of person
        return(self.name)
    
    def get_roles(self):
        return(self.roles)
    
    def get_role(self,role_name):
        try:
            return(self.roles[role_name])
        except KeyError:
            return(None)
            
    def add_role(self,rolename,role):        
        if rolename not in self.roles.keys():
            self.roles[rolename] = role
        return
      
    def remove_role(self,rolename):
        try:
            del self.roles[rolename]
            return
        except KeyError:
            return