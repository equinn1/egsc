from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Pay_check():                                                            #generic check class
    def __init__(self,payperiod,check_number,name,check_date):                #constructor
        self.check_number   = check_number
        self.name           = name
        self.check_date     = check_date
        self.items          = {}
        self.check_id       = None
        self.parent_payperiod = payperiod
        return
    
    def print(self):
        print(self.check_number,self.check_date)
        for i in sorted(self.items.keys()):
            self.items[i].print()
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
    
    def get_parent_payperiod(self):
        return(self.parent_payperiod)
    
    def get_number(self):
        return(self.check_number)
    
    def get_check_id(self):
        return(self.check_id)
    
    def set_check_id(self,ckid):
        self.check_id = ckid
        return
   
    def get_items(self):
        return(self.items)
    
    def add_item(self,check_lineitem):
        item_number = len(self.items) + 1
        self.items[item_number] = check_lineitem
        return(item_number)
    
class Check_lineitem():                                                       #check lineitem class
    def __init__(self,check,fund,acct,obj,position,rate,earnings,acct_desc,obj_desc):
        
        self.parent_check = check               #parent check object
        self.fund = fund                        #accounting info: fund
        self.acct = acct                        #accounting info: acct
        self.obj  = obj                         #accounting info: obj
        self.ftekey = acct+obj                  #fte key for priors
        self.position = position                #position
        self.rate = rate                        #rate
        self.earnings = earnings                #earnings
        self.acct_desc = acct_desc              #acct description
        self.obj_desc = obj_desc                #obj description
        self.acct_UCOA = None                   #UCOA fields
        self.stepinfo  = {}                     #stepinfo
        self.simplex   = None                   #simplex for forecasts

        self.payment_type = None
        self.payment_types = {1:'Contract salary',2:'One-time stipend',3:'Class coverage', \
                      4:'Contract rate',5:'Detention coverage', \
                      6:'Contract salary adjustment', \
                      7:'Contract rate: step 7 stipend',8:'Class coverage', \
                      9:'Other additional compensation', 10:'Contract overtime rate', \
                      11:'Health and Medical',12:'Early Retirement Incentive', \
                      13:'Mentoring',14:'Stipend - Coaches/Advisors',15:'Stipend - other', \
                      16:'Professional Development and Training Services',17:'Class Overage/Weighting', \
                      18:'Stipend - mentors',19:'Coverage - other',20:'Professional Development and Training',  \
                      21:'Summer Pay',22:'Stipend - Athletic Officials',23:'Officials/Referees', \
                      24:'nosuch',25:'Coach/Advisor stipend',26:'Added stipend', \
                      27:'Head custodian stipend - Elementary',28:'Head custodian stipend - Middle School', \
                      29:'Head custodian stipend - High School',30:'Maintenance Foreman stipend', \
                      31:'Head custodian stipend - Elementary - OT',32:'Head custodian stipend - Middle School - OT', \
                      33:'Head custodian stipend - High School - OT',34:'Maintenance Foreman stipend - OT', \
                      35:'Overtime',36:'Facilities stipend',37:'Facilities stipend - OT',38:'Obj 20430', \
                      39:'Custodian part time',40:'Mysterious 1/5/2018', \
                      99:'Other or unknown'}
        
        return
    
    def print(self):
        """Print this check lineitem"""
        print(self.payment_type,self.acct,self.acct_desc,self.obj,self.obj_desc,self.earnings,self.stepinfo)
        return
           
    def get_fund(self):
        """Get fund code"""
        return(self.fund)
            
    def get_acct(self):
        """Get acct code"""
        return(self.acct)
    
    def get_payment_type(self):
        """Get payment type"""
        return(self.payment_type)
    
    def get_parent_check(self):
        """Get parent check object"""
        return(self.parent_check)
    
    def get_payment_types(self):
        """Returns the list of valid type codes"""
        return(self.payment_types)
            
    def get_obj(self):
        """Get obj code"""
        return(self.obj)
            
    def get_ftekey(self):
        """Get fte key for priors"""
        return(self.ftekey)
            
    def get_position(self):
        """Get position object"""
        return(self.position)
        
    def get_rate(self):
        """Get rate from MUNIS report"""
        return(self.rate)
            
    def get_earnings(self):
        """Get earnings from MUNIS report"""
        return(self.earnings)
            
    def get_acct_desc(self):
        """Get acct description"""
        return(self.acct_desc)
            
    def get_obj_desc(self):
        """Get object description"""
        return(self.obj_desc)
            
    def get_acct_UCOA(self):
        """Get acct UCOA codes"""
        return(self.acct_UCOA)
    
    def set_acct_UCOA(self,ucoa):
        """Set acct UCOA codes"""
        self.acct_UCOA = ucoa
        return
                
    def get_simplex(self):
        """Get simplex for forecasts"""
        return(self.simplex)
    
    def set_simplex(self,splx):
        """Set simplex for forecasts"""
        self.simplex = splx
        return
    
    def set_payment_type(self,new_type):
        """Set payment type"""
        payment_type_keys = self.payment_types.keys()
        valid_type = False
        for key in payment_type_keys:
            if (new_type == self.payment_types[key]):
                valid_type = True
        if not valid_type:
            print("Invalid payment type ",new_type," Valid payment_type codes are ",new_type,self.payment_types)
        else:
            self.payment_type = new_type
        return
                    
    def update_stepinfo(self,key,value):
        """Update stepinfo"""
        self.stepinfo[key] = value
        return()
        
    def get_stepinfo(self):
        """Get stepinfo"""
        return(self.stepinfo)
