from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Person():                                                #generic employee class
    def __init__(self,name):                                   #constructor
        self.name = name                                       #name
        self.person_id = None                                  #unique identifier
        self.roles = {}                                        #roles
        self.EYOB = None                                       #estimated year of birth
        self.gender = None                                     #gender 'M','F'
        return
    
    def get_name(self):                                        #return name of person
        return(self.name)
    
    def set_name(self,name):                                   #name change if necessary
        self.name = name
        return
    
    def get_roles(self):
        return(self.roles)
    
    def print(self):
        print(self.name,self.person_id,self.roles)
        return
    
    def get_person_id(self):
        return(self.person_id)
        
    def set_person_id(self,pid):
        self.person_id = pid
        return
    
    def get_EYOB(self):
        return(self.EYOB)
        
    def set_EYOB(self,EYOB):
        self.EYOB = EYOB
        return
    
    def get_gender(self):
        return(self.gender)
        
    def set_gender(self,gender):
        self.gender = gender
        return
    
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