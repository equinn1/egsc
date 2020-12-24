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
    
class Teacher(Person):
    
    def __init__(self, name):
        Person.__init__(self, name) 
        
        self.col_names ={0:'B',1:'B+30',2:'M',3:'M+30',4:'M2/CAGS',5:'D'}

                                                    #get step, FTE, # of payments for teachers
    def decode_earnings(self,ppo,chk,lineitem,salary_matrix):  
        
        dct = {}                                    #dictionary for returned values
        
        obj = lineitem.get_obj()
        rate = lineitem.get_rate()
        in_earnings = lineitem.get_earnings()
        
        if (obj not in ['51110','51132','53204']):  #only these object codes get decoded
            return(dct)
        
        earnings = abs(in_earnings)                 #reverse sign if earnings are negative
                                                   
        f = [1.0,1/2.,1/10.,1/5.,4/5.,3/10.,\
            4/10.,6/10.,1/20.,1/3.,2/3.,1/4.,\
            3/4.,1/5.,2/5.,3/5.,4/5.,1/6.,5/6.,\
            1/7.,2/7.,3/7.,4/7.,5/7.,6/7.,1/8.,\
            3/8.,5/8.,7/8.,1/9.,2/9.,4/9.,5/9.,\
             7/9.,8/9.,7/10.,9/10.]                 #possible FTE fractions list

        salary = round(184.0*rate,2)                #salary is 184 times daily rate
        lower_bound = salary - 1.0                  #lower limit for tolerance
        upper_bound = salary + 1.0                  #upper limit for tolerance
        step_code = ''                              #initialize step code
        n_payments = [26.0,21.0]                    #possible number of payments: 26 or 21  

        fte = np.NaN                                #initialize fte, payments, and min diff
        payments = np.NaN
        min_abs_diff = 10000. 
        
        school_year = ppo.get_school_year()         #get school year from pay period object
            
        sy = int(school_year[5:])                   #second part of school year string
        
        max_earn = salary_matrix[9,5]               #get upper bound for earnings - step D-10
        if (earnings > max_earn):
            print('max exceeded: ',rate,check_date,earnings)
            return(dct)
                                                                #search salary matrix for a match
        for step in np.arange(10):                        #loop through steps
            for col in np.arange(6):                #loop through columns
                cbasal = salary_matrix[step,col]          #salary from CBA matrix

                if( (lower_bound <= cbasal) &\
                    (cbasal <= upper_bound) ):               #computed salary within $1 of CBA
                    col_name = self.col_names[col]
                    step_code = school_year + '-' + col_name + \
                        '-' + str(step+1)    #code is:  yyyy-yyyy-cat-step

        if ((rate > 200.) | (earnings > 1000.)):       #determine fte and payments from rate
            for p in n_payments:                       #loop through payment counts 26 and 21
                for frac in f:                         #loop through the FTE fractions in the list
                    diff = abs(earnings - 184.0*rate*frac/p)    #compute the difference from earnings
                    if (diff < min_abs_diff):                   #see if this is the smallest so far
                        min_abs_diff = diff                     #if it is, then save the min difference
                        payments = p                            #save the number of payments
                        fte = frac                              #save the FTE fraction
        elif ((rate > 0.0) & \
              (rate < 100.) & \
              (earnings > 500.)):                         #do this when rate is too low to be a daily rate
            for p in n_payments:                                #loop through possible payments 26 and 21
                for frac in f:                                  #loop through possible FTE fractions
                    for s in np.arange(10):                 #loop through CBA salary steps
                        for c in np.arange(6):              #loop through salary matrix columns
                            sal = salary_matrix[s,c]        #look up salary in CBA tables
                            try:
                                diff = abs(earnings - frac*sal/p)  #compute delta from earnings
                            except TypeError:
                                diff = 100000.0
                            if (diff < min_abs_diff):       #if this is the smallest difference so far:
                                min_abs_diff = diff         #save the smallest value
                                fte = frac                  #save the FTE fraction
                                mc = self.col_names[c]      #save the salary matrix column
                                salary = sal
                                payments = p                #save the number of payments
                                step_code = school_year + '-' + mc + '-' + str(s+1)  #construct the step code
        dct['step'] = step_code                             #save results in dictionary dct
        dct['payments'] = payments
        dct['fte'] = fte
        dct['mindiff'] = round(min_abs_diff,4)
        dct['salary'] = round(salary,2)
        
        if ((min_abs_diff > 5.0) | (len(step_code) < 2)):   #if diff is too big or not match
            return({})                                     #return empty dictionary
        else:                                              #otherwise return the one we built
            return(dct)