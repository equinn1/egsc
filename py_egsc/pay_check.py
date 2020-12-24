from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Pay_check():                                                            #generic check class
    def __init__(self,check_number,name,check_date):                          #constructor
        self.check_number   = check_number
        self.name           = name
        self.check_date     = check_date
        self.items          = {}
        return

    def get_name(self):
        return(self.name)
    
    def get_school_year(self):
        yy = self.check_date.year
        boundry = date(yy,8,14)
        if (self.check_date <= boundry):
            syear = str(yy-1) + '-' + str(yy)
        else:
            syear = str(yy) + '-' + str(yy + 1)
        return(syear)
        
    def get_date(self):
        return(self.check_date)
    
    def get_number(self):
        return(self.check_number)
   
    def get_items(self):
        return(self.items)
    
    def add_item(self,check_lineitem):
        item_number = len(self.items) + 1
        self.items[item_number] = check_lineitem
        return
    
class Check_lineitem():                                                       #check lineitem class
    def __init__(self,fund,acct,obj,position,rate,earnings,acct_desc,obj_desc):
        self.fund = fund
        self.acct = acct
        self.obj  = obj
        self.position = position
        self.rate = rate
        self.earnings = earnings
        self.acct_desc = acct_desc
        self.obj_desc = obj_desc
        self.acct_UCOA = None
        self.stepinfo = None
        
    def get_fund(self):
        return(self.fund)
            
    def get_acct(self):
        return(self.acct)
            
    def get_obj(self):
        return(self.obj)
            
    def get_position(self):
        return(self.position)
        
    def get_rate(self):
        return(self.rate)
            
    def get_earnings(self):
        return(self.earnings)
            
    def get_acct_desc(self):
        return(self.acct_desc)
            
    def get_obj_desc(self):
        return(self.obj_desc)
            
    def get_acct_UCOA(self):
        return(self.acct_UCOA)
    
    def get_stepinfo(self):
        return(self.stepinfo)
    
    def set_stepinfo(self,sinfo):
        self.stepinfo = sinfo
        return
    
    def set_acct_UCOA(self,ucoa):
        self.acct_UCOA = ucoa
        return