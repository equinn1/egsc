from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
import copy as cp
import pickle

class Role():                                                  #generic employee class
    def __init__(self,person,role_name):                       #constructor
        self.parent_person = person
        self.role_name = role_name                             #role name
        self.payperiods = {}                                   #payperiod objects
        self.first_payperiod = None                            #earliest payperiod object for this role  
        self.first_school_year = None                          #school year of earliest payperiod object
        self.first_school_year_seq = None                      #school year sequence of earliest payperiod object
        self.empirical_priors = {}                             #priors for steps and/or job titles
        self.fte_empirical_priors = {}    
        return
    
    def get_role_name(self):                                   #return role name
        return(self.role_name)
    
    def get_parent_person(self):                               #return parent person
        return(self.parent_person)
    
    def get_empirical_priors(self):                            #return empirical priors
        return(self.empirical_priors)
        
    def get_fte_empirical_priors(self):                               #return parent person
        return(self.fte_empirical_priors)
    
    def get_payperiods(self):                                  #return payperiods dictionary
        return(self.payperiods)
    
    def get_payperiod(self,school_year,seqno):                 #return a specific payperiod
        """ get_payperiod(school_year,sequno)  Returns a specific payperiod by year and sequence"""
        try:
            return(self.payperiods[school_year][seqno])
        except IndexError:
            return({})
        
    def has_payperiod(self,school_year,seqno):                 #check if payperiod is present
        """has_payperiod(school_year,seqno)  Checks for payperiod with given year and sequence"""       
        try:
            pp = self.payperiods[school_year][seqno]
            return(True)
        except KeyError:
            return(False)
        
    def setup_priors(self,lineitem):
        """Generic prior initialization - does nothing.  Roles that use priors implement this"""
        return
            
    def add_payperiod_by_index(self,syear,syseq,pperiod):     #payperiod school year and seqno
        """ add_payperiod_by_index(syear,syseq,pperiod)   Add a new payperiod to the dictionary"""
        if syear not in self.payperiods.keys():               #add school year dictionary if there isn't one already
            self.payperiods[syear] = {}
        if syseq not in self.payperiods[syear].keys():        #add payperiod to school year dictionary with seqence as key
            self.payperiods[syear][syseq] = pperiod
                
        previous_payperiod = None                             #build (or rebuild) chronological chain of payperiods
        self.first_payperiod = None
        for sy in sorted(self.payperiods.keys()):             #process in school year order          
            for sy_seq in sorted(self.payperiods[sy].keys()): #and school year sequence order within a school year
                if (self.first_payperiod is None):
                    self.first_payperiod = self.payperiods[sy][sy_seq]
                    self.first_school_year = self.first_payperiod.get_school_year()
                    self.first_school_year_seq = self.first_payperiod.get_school_year_seq()
                self.payperiods[sy][sy_seq].set_prev_payperiod(previous_payperiod)    #bacwards link to previous
                self.payperiods[sy][sy_seq].set_next_payperiod(None)                  #forward link is None for now
                if (previous_payperiod is not None):                                  #update forward link in previous
                    previous_payperiod.set_next_payperiod(self.payperiods[sy][sy_seq]) 
                previous_payperiod = self.payperiods[sy][sy_seq]                      #set current as previous for next loop
        return
    
    def decode_earnings(self,lineitem):
        """ decode_earnings(lineitem,salary_matrix,x)  Placeholder function for generic role class"""
        dct = {}                                    #dictionary for returned values
        return(dct)
    
    def get_cba_matrix(self):
        return(self.cba)
    
    def get_cba_matrix_by_year(self, school_year):
        return(self.cba[school_year])
    
    def get_first_payperiod(self):
        return(self.first_payperiod)                           #earliest payperiod object for this role
    
    def get_first_school_year(self):
        return(self.first_school_year)                         #school year of earliest payperiod object
    
    def get_first_school_year_seq(self):
        return(self.first_school_year_seq)                     #school year sequence of earliest payperiod object
    
################################################################################################
    
class Teacher(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name)
                
        self.FTE_fractions    = {0:1.0, 1:1/2., 2:1/10., 3:1/5., 4:4/5., 5:3/10., 6:2/5.,\
            7:3/5., 8:1/20., 9:1/3., 10:2/3., 11:1/4., 12:3/4.,13:1/6., 14:5/6., 15:1/7., 16:2/7.,\
            17:3/7., 18:4/7.,19:5/7., 20:6/7., 21:1/8., 22:3/8., 23:5/8., 24:7/8., 25:1/9., 26:2/9.,\
            27:4/9., 28:5/9., 29:7/9., 30:8/9., 31:7/10., 32:9/10.} 
        self.n_payments = {0:26, 1:21}
        self.col_names ={0:'B',1:'B+30',2:'M',3:'M+30',4:'M2/CAGS',5:'D'}
        self.reverse_col_names ={'B':0,'B+30':1,'M':2,'M+30':3,'M2/CAGS':4,'D':5}
      
        self.cba = {}
                                #start with FY2016 (2015-2016) salary matrix
        self.cba['2015-2016'] = np.array([
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
        self.cba['2016-2017'] = self.cba['2015-2016'].copy()
        
                                #FY2018 (2017-2018) 2% increase
        self.cba['2017-2018'] = np.around(1.02*self.cba['2016-2017'].copy(),0)
        
                                #FY2019 (2018-2019) 2.25% increase
        self.cba['2018-2019'] = np.around(1.0225*self.cba['2017-2018'].copy(),0)
        
                                #FY2020 (2019-2020) same as FY2019
        self.cba['2019-2020'] = np.array([
            [43059, 44743, 45755, 46416, 46821, 47127],
            [46798, 48480, 49492, 50150, 50556, 50866],
            [50577, 52258, 53272, 53930, 54336, 54643],
            [54356, 56037, 57049, 57709, 58115, 58424],
            [58137, 59817, 60833, 61490, 61896, 62204],
            [61916, 63598, 64612, 65271, 65679, 65983],
            [65696, 67380, 68390, 69050, 69456, 69765],
            [69477, 71158, 72171, 72804, 72828, 73544],
            [74822, 76504, 77515, 78173, 78581, 78888],
            [82287, 84140, 85254, 85979, 86425, 86763]])     
                                #FY2021 (2020-2021) 2% increase, don't round to dollar
        self.cba['2020-2021'] = np.array([
            [43920.18, 45637.86, 46670.10, 47344.32, 47757.42, 48069.54],
            [47733.96, 49449.60, 50481.84, 51153.00, 51567.12, 51883.32],
            [51588.54, 53303.16, 54337.44, 55008.60, 55422.72, 55735.86],
            [55443.12, 57157.74, 58189.98, 58863.18, 59277.30, 59592.48],
            [59299.74, 61013.34, 62049.66, 62719.80, 63133.92, 63448.08],
            [63154.32, 64869.96, 65904.24, 66576.42, 66992.58, 67302.66],
            [67009.92, 68727.60, 69757.80, 70431.00, 70845.12, 71160.30],
            [70866.54, 72581.16, 73614.42, 74260.08, 74284.56, 75014.88],
            [76318.44, 78034.08, 79065.30, 79736.46, 80152.62, 80465.76],
            [83932.74, 85822.80, 86959.08, 87698.58, 88153.50, 88498.26]])         
                                #FY2022 (2021-2022) 2.25% increase, don't round to dollar
        self.cba['2021-2022'] = np.array([
            [44908.38, 46664.71, 47720.18, 48409.57, 48831.96, 49151.10],
            [48807.97, 50562.22, 51617.68, 52303.94, 52727.38, 53050.69],
            [52749.28, 54502.48, 55560.03, 56246.29, 56669.73, 56989.92],
            [56690.59, 58443.79, 59499.25, 60187.60, 60611.04, 60933.31],
            [60663.98, 62386.14, 63445.78, 64131.00, 64554.43, 64875.66],
            [64575.29, 66329.53, 67387.09, 68074.39, 68499.91, 68816.97],
            [68517.64, 70273.97, 71327.35, 72015.70, 72439.14, 72761.41],
            [72461.04, 74214.24, 75270.74, 75930.93, 75955.96, 76702.71],
            [78035.60, 79789.85, 80844.27, 81530.53, 81956.05, 82276.24],
            [85821.23, 87753.81, 88915.66, 89671.80, 90136.95, 90489.47]])         
                                #FY2023 (2022-2023) same as FY2022
        self.cba['2022-2023'] = self.cba['2021-2022'].copy()        
                                #FY2024 (2023-2024) 2% increase, don't round to dollar
        self.cba['2023-2024'] = np.around(1.02*self.cba['2022-2023'].copy(),2)        
                                #FY2025 (2024-2025) 2.25% increase, don't round to dollar
        self.cba['2024-2025'] = np.around(1.0225*self.cba['2023-2024'].copy(),2)        
                                #FY2015: back out 2.5% increase from FY2016, round to dollar
        self.cba['2014-2015'] = np.around(self.cba['2015-2016'].copy()/1.025,0) 
                                #FY2014: back out 2% increase from FY2015, round to dollar
        self.cba['2013-2014'] = np.around(self.cba['2014-2015'].copy()/1.02,0)  
                                #FY2013: back out 1.01% from FY2014 for steps 1-9, round to dollar
        self.cba['2012-2013'] = self.cba['2013-2014'].copy()
        self.cba['2012-2013'][0:8,:] = np.around(self.cba['2012-2013'][0:8,:]/1.01,0)
                                #FY2013: back out 2.25% from FY2014 for step 10, round to dollar
        self.cba['2012-2013'][9,:]   = np.around(self.cba['2012-2013'][9,:]/1.0225,0)  
        
        with open('../../finance_subcommittee/rate_lookup_.pkl', 'rb') as handle:
            self.rate_lookup =  pickle.load(handle)
            
        with open('../../finance_subcommittee/empirical_priors_1_14_2021.pkl', 'rb') as handle:
            empirical_probabilities = pickle.load(handle)
            
        for key in empirical_probabilities['TEACHER'].keys():
            if (key != 'fte'):
                self.empirical_priors[key] = empirical_probabilities['TEACHER'][key]
        self.fte_empirical_priors = empirical_probabilities['TEACHER']['fte']
        return
            
    def set_cba_matrix(self,cba_matrix):
        self.cba_matrix = cp.deepcopy(cba_matrix)
        return
    
    def set_cba_matrix_by_year(self, school_year,cba_matrix):
        self.cba_matrix[school_year] = cp.deepcopy(cba_matrix)
        return
     
    def get_n_payments(self,i):
        return(n_payments[i])
    
    def get_rate_lookup(self):
        return(self.rate_lookup)
        
    def get_FTE_fraction(self,i):
        return(FTE_fractions[i])
    
    def get_empirical_priors(self):
        pd = cp.deepcopy(self.empirical_priors)
        return(pd)
    
    def get_fte_empirical_priors(self):
        pd = cp.deepcopy(self.fte_empirical_priors)
        return(pd)
    
    def set_empirical_priors(self,prior):
        prior_copy = cp.deepcopy(prior)
        try:
            self.fte_empirical_priors = cp.deepcopy(prior_copy['fte'])
            del prior_copy['fte']
            self.empirical_priors = cp.deepcopy(prior_copy)
        except KeyError:
            print('set empirical priors KeyError',prior_copy)
            return
    
    def update_priors(self,param,n,ppo):
        """update_priors(param,value) updates the priors for param given value"""
        try:
            for i in ppo.priors[param].keys():
                ppo.priors[param][i] = 0.5*ppo.priors[param][i]
        except KeyError:
            print('update_priors KeyError ',ppo.priors)
            return
        try:
            ppo.priors[param][n] += 0.5
        except KeyError:
            print('update_priors KeyError ',param,n)
        return
    
    def update_fte_priors(self,ftekey,n,ppo):
        """Updates prior FTE Dirichlet probabilities"""
        ftep = ppo.get_fte_priors()
        if ftekey not in ftep.keys():            #first entry for this key
            ppo.set_fte_priors_by_key(ftekey,self.fte_empirical_priors)
            
        for i in ppo.fte_priors[ftekey].keys():
            ppo.fte_priors[ftekey][i] = 0.5*ppo.fte_priors[ftekey][i]
        try:
            ppo.fte_priors[ftekey][n] += 0.5
        except KeyError:
            print('update_fte_priors KeyError ',ftekey,n)
            print('fte_priors dictionary ',ppo.fte_priors)
        return                              
    
    #get step, FTE, # of payments for teachers
    
    def decode_earnings(self,lineitem):
       
        fund             = lineitem.get_fund()
        obj              = lineitem.get_obj()
        rate             = lineitem.get_rate()
        acct             = lineitem.get_acct()
        ftekey           = lineitem.get_ftekey()
        in_earnings      = lineitem.get_earnings()
        earnings         = abs(in_earnings)                 #reverse sign if earnings are negative
        
        chk              = lineitem.get_parent_check()      #parent check object
        ppo              = chk.get_parent_payperiod()       #parent payperiod object
        school_year      = ppo.get_school_year()            #school year for current lineitem
        syseq            = ppo.get_school_year_seq()        #school year sequence number
        parent_role      = ppo.get_parent_role()            #get parent role
        rate_lookup      = parent_role.get_rate_lookup()
        payperiods       = parent_role.get_payperiods()
        person           = parent_role.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        payment_type     = 'Other or unknown'
        
        error_tolerance  = 3
                
        if (rate == 0.0):                          #zero rate

            payment_type = "Other or unknown"
            return
        
        elif (obj == '51323'):                       #detention coverage

            payment_type = "Detention coverage"
            if (rate > 0.0):
                hours = round(earnings/rate,2)
                lineitem.update_stepinfo('hours',hours)
            return;
        
        elif (obj == '51327'):                       #other additional compensation

            payment_type = "Other additional compensation"
            if (rate > 0.0):
                hours = round(earnings/rate,2)  
                lineitem.update_stepinfo('hours',hours)
            return
        
                    
        elif rate in rate_lookup[school_year].keys():
            
            col = rate_lookup[school_year][rate]['col']
            self.update_priors('col',col,ppo)
            
            row = rate_lookup[school_year][rate]['row']
            self.update_priors('row',row,ppo)
            
            lineitem.update_stepinfo('step',school_year + '-' + self.col_names[col] + \
                            '-' + str(row+1))        #code is:  yyyy-yyyy-cat-step
            salary = 184.0*rate
            lineitem.update_stepinfo('salary',salary)
            
            priors = ppo.get_priors()
            pmtix = ppo.likelihood_order(priors['payments'])
           
            ftepriors = ppo.get_fte_priors()
            
            if ftekey not in ftepriors.keys():
                ftepriors[ftekey] = self.fte_empirical_priors
                
            fteix = ppo.likelihood_order(ftepriors[ftekey])
        
            within_error_tolerance = False
            
            for i in pmtix:                    #loop through payments
                for j in fteix:                #loop through fte values
                    if (not within_error_tolerance):
                        computed_earnings = salary*self.FTE_fractions[fteix[j]]/\
                            self.n_payments[pmtix[i]]
                        
                        if (abs(earnings - computed_earnings) < error_tolerance):
                        
                            fte = self.FTE_fractions[fteix[j]]
                            self.update_priors('payments',pmtix[i],ppo)
                            self.update_fte_priors(ftekey,fteix[j],ppo)
                            pmts = self.n_payments[pmtix[i]]
                            lineitem.update_stepinfo('payments',pmts)
                            lineitem.update_stepinfo('fte',fte)
                       
                            within_error_tolerance = True                                    
        return
        
class Para(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name) 
        
        self.empirical_priors = {}                             #empirical priors

        self.cba = {
            '2019-2020':{
                'Para':    {7:19.91, 6:18.79, 5:17.86, 4:17.36, 3:16.84, 2:16.48, 1:15.97},
                'Office':  {7:23.76, 6:21.81, 5:20.78, 4:19.76, 3:18.70, 2:17.96, 1:17.44},
                'Central': {7:27.67, 6:25.63, 5:24.57, 4:23.57, 3:22.51, 2:21.78, 1:21.26}
            },
            '2018-2019':{
                'Para':    {7:19.52, 6:18.42, 5:17.51, 4:17.02, 3:16.51, 2:16.16, 1:15.66},
                'Office':  {7:23.29, 6:21.38, 5:20.37, 4:19.37, 3:18.33, 2:17.61, 1:17.10},
                'Central': {7:27.13, 6:25.12, 5:24.09, 4:23.10, 3:22.07, 2:21.35, 1:20.84}
            },
            '2017-2018':{
                'Para':    {7:19.14, 6:18.06, 5:17.17, 4:16.69, 3:16.19, 2:15.84, 1:15.35},
                'Office':  {7:22.83, 6:20.96, 5:19.97, 4:18.99, 3:17.97, 2:17.26, 1:16.76},
                'Central': {7:26.60, 6:24.63, 5:23.62, 4:22.65, 3:21.64, 2:20.93, 1:20.43}
            },
            '2016-2017':{
                'Para':    {7:19.14, 6:18.06, 5:17.17, 4:16.69, 3:16.19, 2:15.84, 1:15.35},
                'Office':  {7:22.83, 6:20.96, 5:19.97, 4:18.99, 3:17.97, 2:17.26, 1:16.76},
                'Central': {7:26.60, 6:24.63, 5:23.62, 4:22.65, 3:21.64, 2:20.93, 1:20.43}
            },
            '2015-2016':{
                'Para':    {7:18.77, 6:17.71, 5:16.83, 4:16.37, 3:15.88, 2:15.53, 1:15.04},
                'Office':  {7:22.38, 6:20.55, 5:19.58, 4:18.62, 3:17.62, 2:16.92, 1:16.43},
                'Central': {7:26.08, 6:24.15, 5:23.16, 4:22.21, 3:21.22, 2:20.52, 1:20.03}
            },
            '2014-2015':{
                'Para':    {7:18.40, 6:17.36, 5:16.50, 4:16.04, 3:15.57, 2:15.23, 1:14.75},
                'Office':  {7:21.94, 6:20.15, 5:19.19, 4:18.25, 3:17.27, 2:16.59, 1:16.11},
                'Central': {7:25.57, 6:23.67, 5:22.70, 4:21.77, 3:20.80, 2:20.12, 1:19.64}
            },
            '2013-2014':{
                'Para':    {7:18.04, 6:17.02, 5:16.18, 4:15.73, 3:15.26, 2:14.93, 1:14.46},
                'Office':  {7:21.51, 6:20.15, 5:19.19, 4:18.25, 3:17.27, 2:16.59, 1:16.11},
                'Central': {7:25.57, 6:23.67, 5:22.70, 4:21.77, 3:20.80, 2:20.12, 1:19.64}
            }
                
        }
        
        with open('../../finance_subcommittee/para_rate_lookup_1_16_2021.pkl', 'rb') as handle:
            self.para_rate_lookup =  pickle.load(handle)
            
        with open('../../finance_subcommittee/para_priors_1_16_2021.pkl', 'rb') as handle:
            self.para_priors =  pickle.load(handle)
            
        self.set_empirical_priors(self.para_priors)
            
        return
    
    def set_empirical_priors(self,prior):
        try:
            self.empirical_priors = cp.deepcopy(prior)
        except KeyError:
            print('Para - set empirical priors KeyError ',prior)
        return
    
    def get_rate_lookup(self):
        return(self.para_rate_lookup)
        
    def update_priors(self,job,n,ppo):
        """update_priors(param,value) updates the priors for param given value"""
        try:
            for i in ppo.priors[job].keys():
                ppo.priors[job][i] = 0.5*ppo.priors[job][i]
        except KeyError:
            print('Para - update_priors KeyError ',job,n,ppo.priors)
            return
        try:
            ppo.priors[job][n] += 0.5
        except KeyError:
            print('Para - update_priors KeyError ',param,n,ppo.priors)
        return
        
    #get step, hours for paras, office, and central office
    
    def decode_earnings(self,lineitem):
       
        fund             = lineitem.get_fund()
        obj              = lineitem.get_obj()
        rate             = lineitem.get_rate()
        acct             = lineitem.get_acct()
        in_earnings      = lineitem.get_earnings()
        earnings         = abs(in_earnings)                 #reverse sign if earnings are negative
        
        chk              = lineitem.get_parent_check()      #parent check object
        ppo              = chk.get_parent_payperiod()       #parent payperiod object
        school_year      = ppo.get_school_year()            #school year for current lineitem
        syseq            = ppo.get_school_year_seq()        #school year sequence number
        parent_role      = ppo.get_parent_role()            #get parent role
        rate_lookup      = self.get_rate_lookup()
        person           = self.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        payment_type     = 'Other or unknown'
        
        error_tolerance  = 3
                
        if (rate == 0.0):                          #zero rate

            payment_type = "Other or unknown"
            return
          
        elif str(rate) in rate_lookup[school_year].keys():
            
            step = rate_lookup[school_year][str(rate)]['step'] - 1
            job = rate_lookup[school_year][str(rate)]['job']
            mindiff = rate_lookup[school_year][str(rate)]['mindiff']
            hours = None
            if (rate > 0.0):
                hours = earnings/rate
            
            self.update_priors(job,step,ppo)
            lineitem.update_stepinfo('step',school_year + '-' + str(step+1))        #code is:  yyyy-yyyy-step
            lineitem.update_stepinfo('hours',hours)    
            lineitem.update_stepinfo('mindiff',mindiff)
            lineitem.update_stepinfo('table_rate',rate)
            lineitem.update_stepinfo('table_job',job)
                                                   
        return
        
class Office(Para):
    
    def __init__(self, person, role_name):
        Para.__init__(self, person, role_name)
        self.set_empirical_priors(self.para_priors)
        return
    
    def set_empirical_priors(self,prior):
        try:
            self.empirical_priors = cp.deepcopy(prior)
        except KeyError:
            print('Office - set empirical priors KeyError ',prior)
        return
    
    def xupdate_priors(self,job,n,ppo):
        """update_priors(param,value) updates the priors for param given value"""
        try:
            for i in ppo.priors[job].keys():
                ppo.priors[job][i] = 0.5*ppo.priors[job][i]
        except KeyError:
            print('Office - update_priors KeyError ',job,n,ppo.priors)
            return
        try:
            ppo.priors[job][n] += 0.5
        except KeyError:
            print('Office update_priors KeyError ',job,n,ppo.priors)
        return
            
class Facilities(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name)
        
        self.empirical_priors     = {}                             #empirical priors
        self.fte_empirical_priors = {}
        
        self.cba = {
            '2019-2020': {
                'Maintenance': {'salary': 42163.65, 'rate': 20.2710},
                'Electrician': {'salary': 59778.57, 'rate': 28.7397},
                'Custodian I': {'salary': 30843.54, 'rate': 14.8286},
                'Custodian II': {'salary': 41773.18, 'rate': 20.0833}
            },
            '2018-2019': {
                'Maintenance': {'salary': 41336.62, 'rate': 19.8734},
                'Electrician': {'salary': 58606.44, 'rate': 28.1762},
                'Custodian I': {'salary': 30018.04, 'rate': 14.4318},
                'Custodian II': {'salary': 40954.09, 'rate': 19.6895}
            },
            '2017-2018': {
                'Maintenance': {'salary': 40526.26, 'rate': 19.4837},
                'Electrician': {'salary': 57456.35, 'rate': 27.6232},
                'Custodian I': {'salary': 29214.57, 'rate': 14.0455},
                'Custodian II': {'salary': 40151.02, 'rate': 19.3034}
            },
            '2016-2017': {
                'Maintenance': {'salary': 41773.18, 'rate': 19.1017},
                'Electrician': {'salary': 56329.7280, 'rate': 27.0816},
                'Custodian I': {'salary': 29214.57, 'rate': 13.6364},
                'Custodian II': {'salary': 40151.02, 'rate': 18.9249}
            },
            '2015-2016': {
                'Maintenance': {'salary': 41773.18, 'rate': 18.7300},
                'Electrician': {'salary': 55225.2480, 'rate': 26.5506},
                'Custodian I': {'salary': 29214.57, 'rate': 13.2400},
                'Custodian II': {'salary': 40151.02, 'rate': 18.5500}
            },
            '2014-2015': {
                'Maintenance': {'salary': 41773.18, 'rate': 18.3600},
                'Electrician': {'salary': 54142.40, 'rate': 26.0300},
                'Custodian I': {'salary': 29214.57, 'rate': 12.7300},
                'Custodian II': {'salary': 40151.02, 'rate': 18.1900}
            },
            '2013-2014': {
                'Maintenance': {'salary': 41773.18, 'rate': 18.3600},
                'Electrician': {'salary': 54142.40, 'rate': 26.0300},
                'Custodian I': {'salary': 29214.57, 'rate': 12.7300},
                'Custodian II': {'salary': 40151.02, 'rate': 18.2900}
            }
        }
        for syear in self.cba.keys():
            for job in self.cba[syear].keys():
                self.cba[syear][job]['ot_rate'] = 1.5*self.cba[syear][job]['rate']
        
        return
    
             #added stipend $650 November, 2018
        
    def get_cba_matrix(self):
        return(self.cba)
    
    def get_rate_lookup(self):
        """Null get_rate_lookup function for facilities"""
        return
    
    def get_cba_matrix_by_year(self, school_year):
        return(self.cba[school_year])     
        
    def set_default_priors(self, priors=None):
        if (priors is None):
            self.default_priors['job'] = self.set_uniform_priors(4)
        else:
            self.default_priors = priors
            
    def set_empirical_priors(self,prior):
        self.empirical_priors = prior['FACILITIES']
        return
        
    def decode_earnings(self,lineitem):
       
        fund             = lineitem.get_fund()
        obj              = lineitem.get_obj()
        rate             = lineitem.get_rate()
        acct             = lineitem.get_acct()
        in_earnings      = lineitem.get_earnings()
        earnings         = abs(in_earnings)                 #reverse sign if earnings are negative
        
        chk              = lineitem.get_parent_check()      #parent check object
        ppo              = chk.get_parent_payperiod()       #parent payperiod object
        school_year      = ppo.get_school_year()            #school year for current lineitem
        syseq            = ppo.get_school_year_seq()        #school year sequence number
        parent_role      = ppo.get_parent_role()            #get parent role
        rate_lookup      = self.get_rate_lookup()
        person           = self.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        payment_type     = 'Other or unknown'
        
        error_tolerance  = 3
                
        if (rate == 0.0):                          #zero rate

            payment_type = "Other or unknown"
            return
          
        elif ((rate > 15.0) & (rate < 30.0)):
            
            mindiff = 1000.0
            min_sy = None
            min_job = None
            min_OT  = None
            
            for sy in self.cba.keys():
                for job in self.cba[sy].keys():
                    diff = abs(rate - self.cba[sy][job]['rate'])
                    if (diff < mindiff):
                        mindiff = diff
                        min_sy = sy
                        min_job = job
                        min_OT = False
                    diff = abs(rate - self.cba[sy][job]['ot_rate'])
                    if (diff < mindiff):
                        mindiff = diff
                        min_sy = sy
                        min_job = job
                        min_OT = True
            
            cba_rate = self.cba[min_sy][min_job]['rate']
            if (rate > 0.0):
                hours = round(earnings/rate,4)

            lineitem.update_stepinfo('cba_rate',cba_rate) 
            lineitem.update_stepinfo('hours',hours)    
            lineitem.update_stepinfo('mindiff',round(mindiff,4))
            lineitem.update_stepinfo('syear',min_sy)
            lineitem.update_stepinfo('job',min_job)
            lineitem.update_stepinfo('OT',min_OT)
            lineitem.update_stepinfo('hours',hours)
                                                   
        return
    
    
    def set_initial_priors(self,ppo,probs=None):
        """Null Prior initialization for facilities"""
        return
    
class Custodian(Facilities):
    
    def __init__(self, person, role_name):
        Facilities.__init__(self, person, role_name)
        
class Maintenance(Facilities):
    
    def __init__(self, person, role_name):
        Facilities.__init__(self, person, role_name)

class Electrician(Facilities):
    
    def __init__(self, person, role_name):
        Facilities.__init__(self, person, role_name)
        
class Substitutes(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name) 
        
    def set_empirical_priors(self,prior=None):
        return
    
    def set_empirical_priors(self,prior):
        self.empirical_priors = prior['PARA']
        return
    
    def get_empirical_priors(self):
        return(self.empirical_priors)
        
class Substitute_teacher(Role):
    
    def __init__(self, person, role_name):
        Substitutes.__init__(self, person, role_name) 
        
class Substitute_para(Role):
    
    def __init__(self, person, role_name):
        Substitutes.__init__(self, person, role_name)
        
class Coach(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name) 