from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Role():                                                  #generic employee class
    def __init__(self,role_name):                              #constructor
        self.role_name = role_name                             #role name
        self.payperiods = {}                                   #payperiod objects
        return
    
    def get_role_name(self):                                   #return role name
        return(self.role_name)
    
    def get_payperiods(self):
        return(self.payperiods)
    
    def get_payperiod(self,school_year,seqno):
        try:
            return(self.payperiods[school_year][seqno])
        except IndexError:
            return({})
        
    def check_payperiod(self,school_year,seqno):
        try:
            pp = self.payperiods[school_year][seqno]
            return(True)
        except KeyError:
            return(False)
            
    def add_payperiod_by_index(self,syear,syseq,pperiod):        #payperiod school year and seqno
        if syear not in self.payperiods.keys():
            self.payperiods[syear] = {}
        if syseq not in self.payperiods[syear].keys():
            self.payperiods[syear][syseq] = pperiod
        return
    
    def decode_earnings(self,ppo,chk,lineitem,salary_matrix):  
        dct = {}                                    #dictionary for returned values
        return(dct)
    
class Teacher(Role):
    
    def __init__(self, role_name):
        Role.__init__(self, role_name) 
        
        self.col_names ={0:'B',1:'B+30',2:'M',3:'M+30',4:'M2/CAGS',5:'D'}

                                                    #get step, FTE, # of payments for teachers
    def decode_earnings(self,ppo,chk,lineitem,salary_matrix):  
        

        
        obj = lineitem.get_obj()
        rate = lineitem.get_rate()
        in_earnings = lineitem.get_earnings()
        earnings = abs(in_earnings)                 #reverse sign if earnings are negative
        stepinfo = {}                               #dictionary for step information
        payment_type = 'Other or unknown'
        
        FTE_fractions = [1.0,1/2.,1/10.,1/5.,4/5.,3/10.,\
            4/10.,6/10.,1/20.,1/3.,2/3.,1/4.,\
            3/4.,1/5.,2/5.,3/5.,4/5.,1/6.,5/6.,\
            1/7.,2/7.,3/7.,4/7.,5/7.,6/7.,1/8.,\
            3/8.,5/8.,7/8.,1/9.,2/9.,4/9.,5/9.,\
             7/9.,8/9.,7/10.,9/10.]                 #possible FTE fractions list
        
        if (obj not in ['51110','51132','53204','51323','51327']): #only these object codes get decoded
            lineitem.set_payment_type(payment_type)
            lineitem.set_stepinfo(stepinfo)
            return
        
        if (obj == '51323'):                       #detention coverage
            stepinfo['rate'] = rate
            if (rate > 0.0):
                stepinfo['hours'] = round(earnings/rate,2)  
            else:
                stepinfo['hours'] = np.NaN
            lineitem.set_payment_type('Detention coverage')
            lineitem.set_stepinfo(stepinfo)
            return
        
        if (obj == '51327'):                       #detention coverage
            stepinfo['rate'] = rate
            if (rate > 0.0):
                stepinfo['hours'] = round(earnings/rate,2)  
            else:
                stepinfo['hours'] = np.NaN
            lineitem.set_payment_type('Other additional compensation')
            lineitem.set_stepinfo(stepinfo)
            return
        
        if ((obj == '51110') & ((rate == 30.00) | (rate == 38.00))):        #Class coverage
            stepinfo['rate'] = rate
            if (rate > 0.0):
                stepinfo['hours'] = round(earnings/rate,2)  
            else:
                stepinfo['hours'] = np.NaN
            lineitem.set_payment_type('Class coverage')
            lineitem.set_stepinfo(stepinfo)
            return
                                    
        salary = round(184.0*rate,2)                #salary is 184 times daily rate
        lower_bound = salary - 4.0                  #lower limit for tolerance
        upper_bound = salary + 4.0                  #upper limit for tolerance
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
            lineitem.set_type(payment_type)
            lineitem.set_stepinfo(stepinfo)
            return
        
        #low hanging fruit:  see if 184 times the rate is in the salary table
        
        mindiff = 10000.0
        min_step = 0
        min_col = 0
        
        for step in np.arange(10):                  #loop through steps
            for col in np.arange(6):                #loop through columns
                salary_diff = abs(salary_matrix[step,col] - salary)
                if (salary_diff < mindiff):
                    mindiff = salary_diff
                    min_step = step
                    min_col = col
            
        if (mindiff < (upper_bound - lower_bound)):   #184*rate matches a contract salary
            col_name = self.col_names[min_col]
            step_code = school_year + '-' + col_name + \
                '-' + str(min_step+1)    #code is:  yyyy-yyyy-cat-step
            try:
                payments = round(salary/earnings,0)
            except ZeroDivisionError:
                payments = None
            if ((payments == 26.0) | (payments == 21.0)):
                stepinfo['step'] = step_code                   # stepinfo
                stepinfo['payments'] = payments
                stepinfo['fte'] = 1.0
                stepinfo['mindiff'] = round(mindiff,4)
                stepinfo['salary'] = round(salary,2)
                lineitem.set_payment_type('Contract salary')
                lineitem.set_stepinfo(stepinfo)
                return
            else:                         #check for 26 to 21 balloon payment
                payperiod_sequence_number = ppo.get_school_year_seq()
                earnings_at_21_payments = salary/21
                earnings_at_26_payments = salary/26
                pp_at_26 = payperiod_sequence_number-1
                adjustment_for_21 = pp_at_26*(earnings_at_21_payments - earnings_at_26_payments)
                balloon_payment = earnings_at_21_payments + adjustment_for_21
                if (abs(balloon_payment - earnings) < 10.0):
                    stepinfo['adjustment'] = round(adjustment_for_21,2)
                    stepinfo['payments'] = 21
                    stepinfo['fte'] = 1.0
                    stepinfo['mindiff'] = round(abs(balloon_payment - earnings),4)
                    stepinfo['salary'] = round(salary,2)
                    lineitem.set_payment_type('Contract salary adjustment')
                    lineitem.set_stepinfo(stepinfo)
                    return


        if ((rate > 200.) | (earnings > 1000.)):       #determine fte and payments from rate
            for p in n_payments:                       #loop through payment counts 26 and 21
                for frac in FTE_fractions:             #loop through the FTE fractions in the list
                    diff = abs(earnings - 184.0*rate*frac/p)    #compute the difference from earnings
                    if (diff < min_abs_diff):                   #see if this is the smallest so far
                        min_abs_diff = diff                     #if it is, then save the min difference
                        payments = p                            #save the number of payments
                        fte = frac                              #save the FTE fraction
        elif ((rate > 0.0) & \
              (rate < 100.) & \
              (earnings > 500.)):                    #do this when rate is too low to be a daily rate
            for p in n_payments:                     #loop through possible payments 26 and 21
                for frac in FTE_fractions:           #loop through possible FTE fractions
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
        
        if ((min_abs_diff > 5.0) | (len(step_code) < 2)):  #if diff is too big or not match
            lineitem.set_payment_type(payment_type)
            lineitem.set_stepinfo({})
            return                                         #return empty dictionary
        else:                                              #otherwise build stepinfo
            stepinfo['step'] = step_code                   #save results in dictionary stepinfo
            stepinfo['payments'] = payments
            stepinfo['fte'] = fte
            stepinfo['mindiff'] = round(min_abs_diff,4)
            stepinfo['salary'] = round(salary,2)
            lineitem.set_payment_type('Contract salary')
            lineitem.set_stepinfo(stepinfo)
            return
        
class Para(Role):
    
    def __init__(self, role_name):
        Role.__init__(self, role_name) 
        
    def decode_earnings(self,ppo,chk,lineitem,salary_matrix):  
        
        obj = lineitem.get_obj()
        rate = lineitem.get_rate()
        in_earnings = lineitem.get_earnings()
        school_year = ppo.get_school_year()
        earnings = abs(in_earnings)                 #reverse sign if earnings are negative
        stepinfo = {}
        payment_type = 'Other or unknown'                   
            
        mindiff = 10000.0
        min_step = None
        min_rate = None
            
        for job in salary_matrix.keys():
            for step in np.arange(1,8):
                diff = abs(rate - salary_matrix[job][step])
                if (diff < mindiff):
                    mindiff = diff
                    min_step = step
                    min_rate = salary_matrix[job][step]
            if (mindiff < 10.0):
                stepinfo['step'] = school_year + '-' + str(min_step)
                stepinfo['rate'] = min_rate
                stepinfo['earnings'] = earnings
                stepinfo['hours'] = round(earnings/min_rate,2)
                payment_type = 'Contract rate'
            elif ((ppo.get_payday() == date(2018,2,2)) & (earnings == 463.15)):
                payment_type = 'Contract rate: step 7 stipend'
                stepinfo['earnings'] = earnings
                    
        lineitem.set_stepinfo(stepinfo)
        lineitem.set_payment_type(payment_type)
        return
                
class Sped_Para(Para):
    
    def __init__(self, role_name):
        Para.__init__(self, role_name)    
        
class Office(Para):
    
    def __init__(self, role_name):
        Para.__init__(self, role_name) 
            
class Facilities(Role):
    
    def __init__(self, role_name):
        Role.__init__(self, role_name) 
        
    def decode_earnings(self,ppo,chk,lineitem,salary_matrix):  
        
        obj = lineitem.get_obj()
        rate = lineitem.get_rate()
        in_earnings = lineitem.get_earnings()
        school_year = ppo.get_school_year()
        earnings = abs(in_earnings)                 #reverse sign if earnings are negative
        stepinfo = {}
        payment_type = 'Other or unknown'
      
        mindiff = 10000.0
        min_job = None
        min_overtime = None
        min_rate = None
            
        for job in salary_matrix.keys():
            for overtime in [True,False]:
                cba_rate = salary_matrix[job]['rate']
                if overtime:
                    cba_rate = round(1.5*cba_rate,4)
                diff = abs(rate - cba_rate)
                if (diff < mindiff):
                    mindiff = diff
                    min_job = job
                    min_overtime = overtime
                    min_rate = cba_rate
        
        if (mindiff < 1.0):
            stepinfo['job'] = min_job
            stepinfo['overtime'] = min_overtime
            stepinfo['rate'] = min_rate
            stepinfo['earnings'] = earnings
            stepinfo['hours'] = round(earnings/rate,2)
            if not min_overtime:
                payment_type = 'Contract rate'
            else:
                payment_type = 'Contract overtime rate'
        
        lineitem.set_payment_type(payment_type)
        lineitem.set_stepinfo(stepinfo)
        return
    
class Substitute(Role):
    
    def __init__(self, role_name):
        Role.__init__(self, role_name) 
    
class Substitute_teacher(Substitute):
    
    def __init__(self, role_name):
        Substitute.__init__(self, role_name) 
        
class Substitute_para(Substitute):
    
    def __init__(self, role_name):
        Substitute.__init__(self, role_name) 
        
class Coach(Role):
    
    def __init__(self, role_name):
        Role.__init__(self, role_name) 