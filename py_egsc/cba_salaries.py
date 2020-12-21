from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
    
class Teacher_salaries():
    def __init__(self):                                       #constructor

        self.cba_cols ={'B': 0,'B+30': 1,'M': 2,'M+30': 3,'M2/CAGS': 4, 'D': 5}
        
        self.cols_cba ={'B': 0,'B+30': 1,'M': 2,\
            'M+30': 3,'M2/CAGS': 4, 'D': 5}               #cba salary matrix columns
        
        self.cba = np.zeros((13, 10, 6))    #salary matrix is 3-D numpy array indexed by: fyear, step, column
        
                                                                #start with FY2016 (2015-2016) salary matrix
        self.cba[3,:,:] = np.array([
            [41286, 42900, 43871, 44505, 44893, 45186],
            [44871, 46484, 47454, 48085, 48474, 48771],
            [48494, 50106, 51078, 51709, 52098, 52393],
            [52118, 53729, 54700, 55332, 55722, 56018],
            [55743, 57354, 58328, 58958, 59347, 59642],
            [59366, 60979, 61951, 62583, 62974, 63266],
            [62991, 64605, 65574, 66206, 66596, 66892],
            [66616, 68228, 69199, 69829, 69806, 70515],
            [71741, 73353, 74323, 74954, 75345, 75639],
            [78898, 80675, 81743, 82438, 82866, 83190]]) 
        
                                                                #FY2017 (2016-2017) is the same as FY2016
        self.cba[4,:,:] = self.cba[3,:,:]
        
                                                                #FY2018 (2017-2018) 2% increase
        self.cba[5,:,:] = np.around(1.02*self.cba[4,:,:],0)
        
                                                                #FY2019 (2018-2019) 2.25% increase
        self.cba[6,:,:] = np.around(1.0225*self.cba[5,:,:],0)
        
                                                                #FY2020 (2019-2020) same as FY2019
        self.cba[7,:,:] = self.cba[6,:,:]
        
                                                                #FY2021 (2020-2021) 2% increase
        self.cba[8,:,:] = np.around(1.02*self.cba[7,:,:],0)
        
                                                                #FY2022 (2021-2022) 2.25% increase
        self.cba[9,:,:] = np.around(1.0225*self.cba[8,:,:],0)
        
                                                                #FY2023 (2022-2023) same as FY2019
        self.cba[10,:,:] = self.cba[9,:,:]
        
                                                                #FY2024 (2023-2024) 2% increase
        self.cba[11,:,:] = np.around(1.02*self.cba[10,:,:],0)
        
                                                                #FY2025 (2024-2025) 2.25% increase
        self.cba[12,:,:] = np.around(1.0225*self.cba[11,:,:],0)

        
                                                                #FY2015: back out 2.5% increase from FY2016
        self.cba[2,:,:] = np.around(self.cba[3,:,:]/1.025,0) 
        
                                                                #FY2014: back out 2% increase from FY2015
        self.cba[1,:,:] = np.around(self.cba[2,:,:]/1.02,0)  
        
                                                                #FY2013: back out 1.01% from FY2014 for steps 1-9
        self.cba[0,0:8,:] = np.around(self.cba[1,0:8,:]/1.01,0)
                                                                #FY2013: back out 2.25% from FY2014 for step 10
        self.cba[0,9,:]   = np.around(self.cba[1,9,:]/1.0225,0)  
        return            
    
    def get_cba_matrix(self):
        return(self.cba)
    
    def get_salary(self,fyear,step,col):                        #look up salary by year, column, step
        """Returns CBA salary given fiscal year, column, and step for FY2013-FY2022."""
        yr = fyear - 2013                                       #year index 0 is 2013
        s  = step-1                                             #step index is one less than the step number
        c = col                                                 #column within the CBA salary matrix
        
        try:
            return self.cba[yr,s,c]                             #return the value if it exists
        except KeyError:                                        #otherwise raise error condition
            print("KeyError in get_salary: ",yr,s,c)
        except IndexError:
            print("IndexError in get_salary: ",yr,s,c)
            
    def get_salary_from_code(self,code):                        #look up salary by code
        """Returns CBA salary given step code for FY2013-FY2022."""
        swords = code.split('-')
        yr = int(swords[0]) - 2013                             #year index 0 is 2013
        step = int(swords[2])
        s  = step-1                                             #step index is one less than the step number
        c = self.cols_cba[swords[1]]                            #column within the CBA salary matrix
        
        try:
            return self.cba[yr,s,c]                             #return the value if it exists
        except KeyError:                                        #otherwise raise error condition
            print("KeyError in get_salary: ",yr,s,c)
        except IndexError:
            print("IndexError in get_salary: ",yr,s,c)
            
    def get_future_salary_from_code(self,code,incr):            #look up salary by code
        """Returns CBA salary given step code for FY2013-FY2022."""
        swords = code.split('-')
        yr = int(swords[0]) + incr - 2013                       #year index 0 is 2013
        c = self.cols_cba[swords[1]]                            #column within the CBA salary matrix
        step = int(swords[2]) + incr                            #step                                    
        if (step > 10):
            step=10
        s  = step-1                                         #step index is one less than the step number
        
        try:
            return self.cba[yr,s,c]                             #return the value if it exists
        except KeyError:                                        #otherwise raise error condition
            print("KeyError in get_salary: ",yr,s,c)
        except IndexError:
            print("IndexError in get_salary: ",yr,s,c)
        
    def get_future_code_from_code(self,code,incr):            #look up salary by code
        """Returns CBA salary given step code for FY2013-FY2022."""
        swords = code.split('-')
        yr = int(swords[0]) + incr                              #year index 0 is 2013
        step = int(swords[2]) + incr                            #step                                    
        if (step > 10):
            step=10
        newcode = str(yr) +'-'+ swords[1] + '-' + str(step)    #step index is one less than the step number

        return(newcode)                                         #return the value if it exists
    def decode_earnings(self,check_date,rate,in_earnings,obj):  #get step, FTE, # of payments for teachers
        
        dct = {}
        
        if (obj not in ['51110','51132','53204']):
            return(dct)
        
        earnings = abs(in_earnings)                    #reverse sign if earnings are negative
        
        f = [1.0,1/2.,1/10.,1/5.,4/5.,3/10.,\
            4/10.,6/10.,1/20.,1/3.,2/3.,1/4.,\
            3/4.,1/5.,2/5.,3/5.,4/5.,1/6.,5/6.,\
            1/7.,2/7.,3/7.,4/7.,5/7.,6/7.,1/8.,\
            3/8.,5/8.,7/8.,1/9.,2/9.,4/9.,5/9.,\
             7/9.,8/9.,7/10.,9/10.]                    #possible FTE fractions

        salary = round(184.0*rate,0)                            #salary is 184 times daily rate
        lower_bound = salary - 1.0                              #lower limit for tolerance
        upper_bound = salary + 1.0                              #upper limit for tolerance
        step_code = ''                                          #initialize step code
        n_payments = [26.0,21.0]                                #possible number of payments: 26 or 21                              
        fte = np.NaN
        payments = np.NaN
        min_abs_diff = 10000. 
        
        mm = check_date.month
        fyear = check_date.year
        if (mm > 6):
            fyear += 1
            
        yy = check_date.year
        boundary = date(yy,8,14)
        if (check_date <= boundary):
            school_year_string = str(yy-1) + '-' + str(yy)
        else:
            school_year_string = str(yy) + '-' + str(yy+1)
            
        sy = int(school_year_string[5:])               #
        
        sy_D10_code = str(sy)+'-D-10'
        sy_D10_salary = self.get_salary_from_code(sy_D10_code)
        max_earn = sy_D10_salary/21.0
        if (earnings > max_earn):
            print('max exceeded: ',rate,check_date,earnings)
            return(dct)
                                                                #search salary matrix for a match
        for step in np.arange(1,11):                        #loop through steps
            for col in self.cba_cols.keys():                #loop through columns
                cbasal = self.get_salary(sy,\
                    step,self.cba_cols[col])                #salary from CBA matrix
                if( (lower_bound <= cbasal) &\
                    (cbasal <= upper_bound) ):               #computed salary within $1 of CBA
                    step_code = str(sy) + '-' + col + '-' + str(step)    #code is:  yyyy-cat-step

        if ((rate > 200.) | (earnings > 1000.)):       #determine fte and payments from rate
            for p in n_payments:                                #loop through payments 26 and 21
                for frac in f:                                  #loop through the FTE fractions in the list
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
                        for c in self.cols_cba.keys():            #loop through salary matrix columns
                            sal = self.get_salary(sy,s+1,self.cols_cba[c])    #look up salary in CBA tables
                            try:
                                diff = abs(earnings - frac*sal/p)      #compute delta from earnings
                            except TypeError:
                                diff = 100000.0
                            if (diff < min_abs_diff):       #if this is the smallest difference so far:
                                min_abs_diff = diff         #save the smallest value
                                fte = frac                  #save the FTE fraction
                                mc = c                      #save the salary matrix column
                                yr = sy                     #save the year used for the CBA salary
                                salary = sal
                                payments = p                #save the number of payments
                                step_code = str(yr) + '-' + mc + '-' + str(s+1)  #construct the step code
        dct['step'] = step_code                                 #save results in Teacher object textbox
        dct['payments'] = payments
        dct['fte'] = fte
        dct['mindiff'] = round(min_abs_diff,4)
        dct['salary'] = round(salary,0)
        
        if (min_abs_diff > 5.0):
            return({})
        elif (len(step_code) < 2):
            return({})
        else:
            return(dct)