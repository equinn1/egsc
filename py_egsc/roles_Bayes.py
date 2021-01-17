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
        if self.first_payperiod is None:                      #if no earliest payperiod, use this one as initial value
            self.first_payperiod = pperiod                    #save earliest payperiod object
            self.first_school_year = syear                    #save earliest school year
            self.first_school_year_seq = syseq                #save sequence number in earliest school year
        else:                                                 #earliest payperiod is coded, make sure this one is not earlier
            if ((syear  <  self.first_school_year) |\
                ((syear == self.first_school_year) &\
                 (syseq <  self.first_school_year_seq))):     #if earlier school year, or same school year and earlier seq
                self.first_payperiod = pperiod                # then replace previous earliest payperiod with this one
                self.first_school_year = syear
                self.first_school_year_seq = syseq
                
        previous_payperiod = None                             #build (or rebuild) chronological chain of payperiods
        for sy in sorted(self.payperiods.keys()):             #process in school year order          
            for sy_seq in sorted(self.payperiods[sy].keys()): #and school year sequence order within a school year
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
            
#        with open('../../rate_lookup_1_12.pkl', 'rb') as handle:
#            self.rate_lookup =  pickle.load(handle)
            
        with open('../../finance_subcommittee/empirical_priors_1_14_2021.pkl', 'rb') as handle:
            empirical_probabilities = pickle.load(handle)
        for key in empirical_probabilities['TEACHER'].keys():
            if (key != 'fte'):
                self.empirical_priors[key] = empirical_probabilities['TEACHER'][key]
        self.fte_empirical_priors = empirical_probabilities['TEACHER']['fte']
        return
    
    def add_payperiod_by_index(self,syear,syseq,pperiod):
        super().add_payperiod_by_index(syear,syseq,pperiod)
        prevpp = pperiod.get_prev_payperiod()
        if (prevpp is not None):
            pperiod.priors = cp.deepcopy(prevpp.get_priors())
            pperiod.fte_priors = cp.deepcopy(prevpp.get_fte_priors())
        else:
            pperiod.priors = cp.deepcopy(self.get_empirical_priors())
            pperiod.fte_priors = {}
            
        
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
        self.fte_empirical_priors = {}        
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
                'Office':  {7:21.94, 6:20.15, 5:19.19, 4:18.25, 3:17.27, 2:16.59, 1:16.11},
                'Central': {7:25.57, 6:23.67, 5:22.70, 4:21.77, 3:20.80, 2:20.12, 1:19.64}
            }
                
        }
        return
        
    def set_default_priors(self, priors=None):
        """Generic prior initialization for supplied payperiod object - returns empty dictionary"""
        if (priors is None):
            self.default_priors['job'] = self.set_uniform_priors(3)
            self.default_priors['step'] = self.set_uniform_priors(7)
        else:
            self.default_priors = cp.deepcopy(priors)
        return
    
    def set_empirical_priors(self,prior):
        self.empirical_priors = cp.deepcopy(prior['PARA'])
        return
        
    def decode_earnings(self,lineitem):
        """ decode_earnings(lineitem,salary_matrix)  code step, FTE, and payments for Paras"""
        return
    
        def set_initial_priors(self,ppo):
            """Prior initialization as default for PARA roles"""
            ppo.set_priors(self.default_priors)
            return
        
class Office(Para):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name)
        
        self.default_priors = {}
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
        
        return
    
             #added stipend $650 November, 2018
        
    def get_cba_matrix(self):
        return(self.cba)
    
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
        """ decode_earnings(lineitem,salary_matrix)  code step, FTE, and payments for facilities"""

        return
    
    
        def set_initial_priors(self,ppo,probs=None):
            """Prior initialization for FACILITIES roles as discrete uniform with equal probabilities"""
            if (probs is None):
                ppo.set_priors(self.default_priors)
            else:
                ppo.set_priors(self.default_priors)
            return
    
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
        
{'2013-2014': {
    419.3696: {'row': 9,'col': 1,'salary': 77164.0,'mindiff': 0.0063999999983934686},
    265.5163: {'row': 2,'col': 2,'salary': 48855.0,'mindiff': 0.000800000001618173},
    410.1359: {'row': 9,'col': 0,
   'salary': 75465.0,
   'mindiff': 0.005600000004051253},
  359.712: {'row': 7,
   'col': 2,
   'salary': 66187.0,
   'mindiff': 0.008000000001629815},
  424.9185: {'row': 9,
   'col': 2,
   'salary': 78185.0,
   'mindiff': 0.004000000000814907},
  430.7609: {'row': 9,
   'col': 4,
   'salary': 79260.0,
   'mindiff': 0.005600000004051253},
  303.2011: {'row': 4,
   'col': 2,
   'salary': 55789.0,
   'mindiff': 0.0023999999975785613},
  327.4457: {'row': 6,
   'col': 0,
   'salary': 60250.0,
   'mindiff': 0.00879999999597203},
  386.3533: {'row': 8,
   'col': 2,
   'salary': 71088.0,
   'mindiff': 1.0071999999927357},
  428.5326: {'row': 9,
   'col': 3,
   'salary': 78850.0,
   'mindiff': 0.001600000003236346},
  322.038: {'row': 5,
   'col': 2,
   'salary': 59255.0,
   'mindiff': 0.008000000001629815},
  346.288: {'row': 7,
   'col': 0,
   'salary': 63717.0,
   'mindiff': 0.008000000001629815},
  214.6141: {'row': 0,
   'col': 0,
   'salary': 39489.0,
   'mindiff': 0.005599999996775296},
  246.6739: {'row': 1,
   'col': 2,
   'salary': 45389.0,
   'mindiff': 1.0023999999975786},
  289.7663: {'row': 4,
   'col': 0,
   'salary': 53317.0,
   'mindiff': 0.000800000001618173},
  432.4457: {'row': 9,
   'col': 5,
   'salary': 79570.0,
   'mindiff': 0.00879999999597203},
  303.2012: {'row': 4,
   'col': 2,
   'salary': 55789.0,
   'mindiff': 0.02079999999841675},
  214.6143: {'row': 0,
   'col': 0,
   'salary': 39489.0,
   'mindiff': 0.031199999997625127},
  308.5978: {'row': 5,
   'col': 0,
   'salary': 56782.0,
   'mindiff': 0.004799999995157123},
  316.9837: {'row': 5,
   'col': 1,
   'salary': 58325.0,
   'mindiff': 0.000800000001618173},
  252.0815: {'row': 2,
   'col': 0,
   'salary': 46383.0,
   'mindiff': 0.004000000000814907},
  381.3098: {'row': 8,
   'col': 1,
   'salary': 70161.0,
   'mindiff': 0.003200000006472692},
  260.4674: {'row': 2,
   'col': 1,
   'salary': 47925.0,
   'mindiff': 1.0016000000032363},
  270.9239: {'row': 3,
   'col': 0,
   'salary': 49850.0,
   'mindiff': 0.0023999999975785613},
  279.2989: {'row': 3,
   'col': 1,
   'salary': 51391.0,
   'mindiff': 0.0023999999975785613},
  284.3424: {'row': 3,
   'col': 2,
   'salary': 52320.0,
   'mindiff': 0.9983999999967637},
  372.9239: {'row': 8,
   'col': 0,
   'salary': 68619.0,
   'mindiff': 1.0023999999975786},
  340.8696: {'row': 6,
   'col': 2,
   'salary': 62721.0,
   'mindiff': 0.9936000000016065},
  308.5: {'row': 4, 'col': 4, 'salary': 56765.0, 'mindiff': 1.0},
  428.53: {'row': 9,
   'col': 3,
   'salary': 78850.0,
   'mindiff': 0.4800000000104774},
  228.0489: {'row': 0,
   'col': 2,
   'salary': 41962.0,
   'mindiff': 1.0023999999975786}},
 '2014-2015': {427.7554: {'row': 9,
   'col': 1,
   'salary': 78707.0,
   'mindiff': 0.0063999999983934686},
  290.0272: {'row': 3,
   'col': 2,
   'salary': 53366.0,
   'mindiff': 0.9952000000048429},
  418.337: {'row': 9,
   'col': 0,
   'salary': 76974.0,
   'mindiff': 0.008000000001629815},
  433.4185: {'row': 9,
   'col': 2,
   'salary': 79749.0,
   'mindiff': 0.004000000000814907},
  394.0815: {'row': 8,
   'col': 2,
   'salary': 72510.0,
   'mindiff': 0.9959999999991851},
  270.8261: {'row': 2,
   'col': 2,
   'salary': 49832.0,
   'mindiff': 0.0023999999975785613},
  439.375: {'row': 9, 'col': 4, 'salary': 80845.0, 'mindiff': 0.0},
  437.1033: {'row': 9,
   'col': 3,
   'salary': 80427.0,
   'mindiff': 0.007199999992735684},
  328.4783: {'row': 5,
   'col': 2,
   'salary': 60440.0,
   'mindiff': 0.0072000000000116415},
  257.125: {'row': 2, 'col': 0, 'salary': 47311.0, 'mindiff': 0.0},
  353.212: {'row': 7,
   'col': 0,
   'salary': 64991.0,
   'mindiff': 0.008000000001629815},
  347.6848: {'row': 6,
   'col': 2,
   'salary': 63975.0,
   'mindiff': 0.9968000000008033},
  380.3859: {'row': 8,
   'col': 0,
   'salary': 69991.0,
   'mindiff': 0.005600000004051253},
  237.913: {'row': 1,
   'col': 0,
   'salary': 43777.0,
   'mindiff': 1.0080000000016298},
  314.7717: {'row': 5,
   'col': 0,
   'salary': 57918.0,
   'mindiff': 0.0072000000000116415},
  441.0924: {'row': 9,
   'col': 5,
   'salary': 81161.0,
   'mindiff': 0.001600000003236346},
  333.9946: {'row': 6,
   'col': 0,
   'salary': 61455.0,
   'mindiff': 0.0063999999983934686},
  309.2663: {'row': 4,
   'col': 2,
   'salary': 56905.0,
   'mindiff': 0.000800000001618173},
  366.9076: {'row': 7,
   'col': 2,
   'salary': 67511.0,
   'mindiff': 0.001600000003236346},
  342.5543: {'row': 6,
   'col': 1,
   'salary': 63029.0,
   'mindiff': 0.991200000004028},
  276.3424: {'row': 3,
   'col': 0,
   'salary': 50847.0,
   'mindiff': 0.001600000003236346},
  323.3261: {'row': 5,
   'col': 1,
   'salary': 59492.0,
   'mindiff': 0.0023999999975785613},
  284.8859: {'row': 3,
   'col': 1,
   'salary': 52419.0,
   'mindiff': 0.005599999996775296},
  295.5598: {'row': 4,
   'col': 0,
   'salary': 54383.0,
   'mindiff': 0.0031999999991967343},
  304.1033: {'row': 4,
   'col': 1,
   'salary': 55955.0,
   'mindiff': 0.0072000000000116415},
  399.4946: {'row': 8,
   'col': 4,
   'salary': 73507.0,
   'mindiff': 0.0063999999983934686},
  366.91: {'row': 7,
   'col': 2,
   'salary': 67511.0,
   'mindiff': 0.4400000000023283},
  333.9022: {'row': 5,
   'col': 4,
   'salary': 61438.0,
   'mindiff': 0.004799999995157123},
  433.42: {'row': 9,
   'col': 2,
   'salary': 79749.0,
   'mindiff': 0.27999999999883585},
  251.6088: {'row': 1,
   'col': 2,
   'salary': 46297.0,
   'mindiff': 0.9807999999975436},
  258.5978: {'row': 1,
   'col': 5,
   'salary': 47581.0,
   'mindiff': 0.9952000000048429},
  251.6087: {'row': 1,
   'col': 2,
   'salary': 46297.0,
   'mindiff': 0.9991999999983818},
  433.4183: {'row': 9,
   'col': 2,
   'salary': 79749.0,
   'mindiff': 0.03280000000086147}},
 '2015-2016': {438.4511: {'row': 9,
   'col': 1,
   'salary': 80675,
   'mindiff': 0.0023999999975785613},
  317.0: {'row': 4, 'col': 2, 'salary': 58328, 'mindiff': 0.0},
  428.7935: {'row': 9,
   'col': 0,
   'salary': 78898,
   'mindiff': 0.004000000000814907},
  444.2554: {'row': 9,
   'col': 2,
   'salary': 81743,
   'mindiff': 0.0063999999983934686},
  297.2826: {'row': 3,
   'col': 2,
   'salary': 54700,
   'mindiff': 0.001600000003236346},
  450.3587: {'row': 9,
   'col': 4,
   'salary': 82866,
   'mindiff': 0.0007999999943422154},
  448.0326: {'row': 9,
   'col': 3,
   'salary': 82438,
   'mindiff': 0.001600000003236346},
  356.3804: {'row': 6,
   'col': 2,
   'salary': 65574,
   'mindiff': 0.0063999999983934686},
  283.25: {'row': 3, 'col': 0, 'salary': 52118, 'mindiff': 0.0},
  389.8967: {'row': 8,
   'col': 0,
   'salary': 71741,
   'mindiff': 0.007199999992735684},
  376.0815: {'row': 7,
   'col': 2,
   'salary': 69199,
   'mindiff': 0.004000000000814907},
  257.9022: {'row': 1,
   'col': 2,
   'salary': 47454,
   'mindiff': 0.004799999995157123},
  263.5543: {'row': 2,
   'col': 0,
   'salary': 48494,
   'mindiff': 0.00879999999597203},
  342.3424: {'row': 6,
   'col': 0,
   'salary': 62991,
   'mindiff': 0.001600000003236346},
  444.2555: {'row': 9,
   'col': 2,
   'salary': 81743,
   'mindiff': 0.012000000002444722},
  452.1196: {'row': 9,
   'col': 5,
   'salary': 83190,
   'mindiff': 0.0063999999983934686},
  362.0435: {'row': 7,
   'col': 0,
   'salary': 66616,
   'mindiff': 0.004000000000814907},
  336.6902: {'row': 5,
   'col': 2,
   'salary': 61951,
   'mindiff': 0.0031999999991967343},
  403.9293: {'row': 8,
   'col': 2,
   'salary': 74323,
   'mindiff': 0.00879999999597203},
  370.8043: {'row': 7,
   'col': 1,
   'salary': 68228,
   'mindiff': 0.00879999999597203},
  302.9511: {'row': 4,
   'col': 0,
   'salary': 55743,
   'mindiff': 0.0023999999975785613},
  263.5544: {'row': 2,
   'col': 0,
   'salary': 48494,
   'mindiff': 0.009599999997590203},
  444.2552: {'row': 9,
   'col': 2,
   'salary': 81743,
   'mindiff': 0.04320000000006985},
  322.6413: {'row': 5,
   'col': 0,
   'salary': 59366,
   'mindiff': 0.000800000001618173},
  331.4076: {'row': 5,
   'col': 1,
   'salary': 60979,
   'mindiff': 0.001600000003236346},
  444.26: {'row': 9, 'col': 2, 'salary': 81743, 'mindiff': 0.8399999999965075},
  361.9348: {'row': 6,
   'col': 4,
   'salary': 66596,
   'mindiff': 0.003200000006472692},
  379.38: {'row': 7,
   'col': 4,
   'salary': 69806,
   'mindiff': 0.08000000000174623},
  389.9: {'row': 8, 'col': 0, 'salary': 71741, 'mindiff': 0.5999999999912689},
  277.5979: {'row': 2,
   'col': 2,
   'salary': 51078,
   'mindiff': 0.01359999999840511},
  284.7446: {'row': 2,
   'col': 5,
   'salary': 52393,
   'mindiff': 0.0063999999983934686},
  277.5978: {'row': 2,
   'col': 2,
   'salary': 51078,
   'mindiff': 0.004799999995157123},
  224.3804: {'row': 0,
   'col': 0,
   'salary': 41286,
   'mindiff': 0.0063999999983934686},
  277.6: {'row': 2, 'col': 2, 'salary': 51078, 'mindiff': 0.4000000000014552},
  257.9021: {'row': 1,
   'col': 2,
   'salary': 47454,
   'mindiff': 0.01359999999840511},
  243.8641: {'row': 1,
   'col': 0,
   'salary': 44871,
   'mindiff': 0.005599999996775296}},
 '2016-2017': {438.4511: {'row': 9,
   'col': 1,
   'salary': 80675,
   'mindiff': 0.0023999999975785613},
  336.6902: {'row': 5,
   'col': 2,
   'salary': 61951,
   'mindiff': 0.0031999999991967343},
  428.7935: {'row': 9,
   'col': 0,
   'salary': 78898,
   'mindiff': 0.004000000000814907},
  444.2554: {'row': 9,
   'col': 2,
   'salary': 81743,
   'mindiff': 0.0063999999983934686},
  317.0: {'row': 4, 'col': 2, 'salary': 58328, 'mindiff': 0.0},
  450.3587: {'row': 9,
   'col': 4,
   'salary': 82866,
   'mindiff': 0.0007999999943422154},
  448.0326: {'row': 9,
   'col': 3,
   'salary': 82438,
   'mindiff': 0.001600000003236346},
  376.0815: {'row': 7,
   'col': 2,
   'salary': 69199,
   'mindiff': 0.004000000000814907},
  302.9511: {'row': 4,
   'col': 0,
   'salary': 55743,
   'mindiff': 0.0023999999975785613},
  403.9293: {'row': 8,
   'col': 2,
   'salary': 74323,
   'mindiff': 0.00879999999597203},
  277.5978: {'row': 2,
   'col': 2,
   'salary': 51078,
   'mindiff': 0.004799999995157123},
  283.25: {'row': 3, 'col': 0, 'salary': 52118, 'mindiff': 0.0},
  362.0435: {'row': 7,
   'col': 0,
   'salary': 66616,
   'mindiff': 0.004000000000814907},
  452.1196: {'row': 9,
   'col': 5,
   'salary': 83190,
   'mindiff': 0.0063999999983934686},
  389.8967: {'row': 8,
   'col': 0,
   'salary': 71741,
   'mindiff': 0.007199999992735684},
  356.3804: {'row': 6,
   'col': 2,
   'salary': 65574,
   'mindiff': 0.0063999999983934686},
  398.6576: {'row': 8,
   'col': 1,
   'salary': 73353,
   'mindiff': 0.001600000003236346},
  322.6413: {'row': 5,
   'col': 0,
   'salary': 59366,
   'mindiff': 0.000800000001618173},
  351.1141: {'row': 6,
   'col': 1,
   'salary': 64605,
   'mindiff': 0.005599999996775296},
  263.5543: {'row': 2,
   'col': 0,
   'salary': 48494,
   'mindiff': 0.00879999999597203},
  257.9022: {'row': 1,
   'col': 2,
   'salary': 47454,
   'mindiff': 0.004799999995157123},
  379.3804: {'row': 7,
   'col': 4,
   'salary': 69806,
   'mindiff': 0.0063999999983934686},
  444.255: {'row': 9,
   'col': 2,
   'salary': 81743,
   'mindiff': 0.08000000000174623},
  297.2826: {'row': 3,
   'col': 2,
   'salary': 54700,
   'mindiff': 0.001600000003236346},
  304.4457: {'row': 3,
   'col': 5,
   'salary': 56018,
   'mindiff': 0.00879999999597203},
  243.8641: {'row': 1,
   'col': 0,
   'salary': 44871,
   'mindiff': 0.005599999996775296},
  448.0325: {'row': 9,
   'col': 3,
   'salary': 82438,
   'mindiff': 0.01999999998952262},
  238.4293: {'row': 0,
   'col': 2,
   'salary': 43871,
   'mindiff': 0.00879999999597203},
  224.3804: {'row': 0,
   'col': 0,
   'salary': 41286,
   'mindiff': 0.0063999999983934686},
  233.1522: {'row': 0,
   'col': 1,
   'salary': 42900,
   'mindiff': 0.004799999995157123},
  243.8643: {'row': 1,
   'col': 0,
   'salary': 44871,
   'mindiff': 0.031199999997625127},
  243.864: {'row': 1,
   'col': 0,
   'salary': 44871,
   'mindiff': 0.023999999997613486},
  438.451: {'row': 9,
   'col': 1,
   'salary': 80675,
   'mindiff': 0.01600000000325963},
  272.3152: {'row': 2,
   'col': 1,
   'salary': 50106,
   'mindiff': 0.0031999999991967343},
  224.3803: {'row': 0,
   'col': 0,
   'salary': 41286,
   'mindiff': 0.02479999999923166}},
 '2017-2018': {363.5054: {'row': 6,
   'col': 2,
   'salary': 66885.0,
   'mindiff': 0.0063999999983934686},
  437.3696: {'row': 9,
   'col': 0,
   'salary': 80476.0,
   'mindiff': 0.0063999999983934686},
  453.1413: {'row': 9,
   'col': 2,
   'salary': 83378.0,
   'mindiff': 0.0007999999943422154},
  343.4239: {'row': 5,
   'col': 2,
   'salary': 63190.0,
   'mindiff': 0.0023999999975785613},
  459.3641: {'row': 9,
   'col': 4,
   'salary': 84523.0,
   'mindiff': 0.005600000004051253},
  456.9946: {'row': 9,
   'col': 3,
   'salary': 84087.0,
   'mindiff': 0.0063999999983934686},
  412.0054: {'row': 8,
   'col': 2,
   'salary': 75809.0,
   'mindiff': 0.0063999999983934686},
  447.2228: {'row': 9,
   'col': 1,
   'salary': 82288.0,
   'mindiff': 0.9952000000048429},
  329.0924: {'row': 5,
   'col': 0,
   'salary': 60553.0,
   'mindiff': 0.001600000003236346},
  303.2283: {'row': 3,
   'col': 2,
   'salary': 55794.0,
   'mindiff': 0.0072000000000116415},
  309.0109: {'row': 4,
   'col': 0,
   'salary': 56858.0,
   'mindiff': 0.005599999996775296},
  323.3424: {'row': 4,
   'col': 2,
   'salary': 59495.0,
   'mindiff': 0.001600000003236346},
  397.6957: {'row': 8,
   'col': 0,
   'salary': 73176.0,
   'mindiff': 0.00879999999597203},
  461.163: {'row': 9,
   'col': 5,
   'salary': 84854.0,
   'mindiff': 0.008000000001629815},
  309.0108: {'row': 4,
   'col': 0,
   'salary': 56858.0,
   'mindiff': 0.012799999996786937},
  383.6033: {'row': 7,
   'col': 2,
   'salary': 70583.0,
   'mindiff': 0.007199999992735684},
  349.1902: {'row': 6,
   'col': 0,
   'salary': 64251.0,
   'mindiff': 0.0031999999991967343},
  378.2228: {'row': 7,
   'col': 1,
   'salary': 69593.0,
   'mindiff': 0.004799999995157123},
  349.1903: {'row': 6,
   'col': 0,
   'salary': 64251.0,
   'mindiff': 0.015199999994365498},
  288.913: {'row': 3,
   'col': 0,
   'salary': 53160.0,
   'mindiff': 0.008000000001629815},
  283.1522: {'row': 2,
   'col': 2,
   'salary': 52100.0,
   'mindiff': 0.004799999995157123},
  268.8261: {'row': 2,
   'col': 0,
   'salary': 49464.0,
   'mindiff': 0.0023999999975785613},
  263.0598: {'row': 1,
   'col': 2,
   'salary': 48403.0,
   'mindiff': 0.0031999999991967343},
  228.8696: {'row': 0,
   'col': 0,
   'salary': 42112.0,
   'mindiff': 0.0063999999983934686},
  363.5055: {'row': 6,
   'col': 2,
   'salary': 66885.0,
   'mindiff': 0.012000000002444722},
  257.6848: {'row': 1,
   'col': 1,
   'salary': 47414.0,
   'mindiff': 0.0031999999991967343},
  248.7391: {'row': 1,
   'col': 0,
   'salary': 45768.0,
   'mindiff': 0.005599999996775296},
  243.1957: {'row': 0,
   'col': 2,
   'salary': 44748.0,
   'mindiff': 0.00879999999597203},
  390.8967: {'row': 7,
   'col': 5,
   'salary': 71925.0,
   'mindiff': 0.007199999992735684}},
 '2018-2019': {392.2337: {'row': 7,
   'col': 2,
   'salary': 72171.0,
   'mindiff': 0.0007999999943422154},
  447.212: {'row': 9,
   'col': 0,
   'salary': 82287.0,
   'mindiff': 0.008000000001629815},
  463.337: {'row': 9,
   'col': 2,
   'salary': 85254.0,
   'mindiff': 0.008000000001629815},
  371.6848: {'row': 6,
   'col': 2,
   'salary': 68390.0,
   'mindiff': 0.003200000006472692},
  469.7011: {'row': 9,
   'col': 4,
   'salary': 86425.0,
   'mindiff': 0.0023999999975785613},
  467.2772: {'row': 9,
   'col': 3,
   'salary': 85979.0,
   'mindiff': 0.004799999995157123},
  457.2826: {'row': 9,
   'col': 1,
   'salary': 84139.0,
   'mindiff': 0.9983999999967637},
  336.5: {'row': 5, 'col': 0, 'salary': 61915.0, 'mindiff': 1.0},
  357.0435: {'row': 6,
   'col': 0,
   'salary': 65697.0,
   'mindiff': 0.9959999999991851},
  330.6141: {'row': 4,
   'col': 2,
   'salary': 60834.0,
   'mindiff': 1.0055999999967753},
  447.2228: {'row': 9,
   'col': 0,
   'salary': 82287.0,
   'mindiff': 1.9952000000048429},
  351.1522: {'row': 5,
   'col': 2,
   'salary': 64612.0,
   'mindiff': 0.004799999995157123},
  471.538: {'row': 9,
   'col': 5,
   'salary': 86763.0,
   'mindiff': 0.008000000001629815},
  421.2772: {'row': 8,
   'col': 2,
   'salary': 77515.0,
   'mindiff': 0.004799999995157123},
  377.5924: {'row': 7,
   'col': 0,
   'salary': 69477.0,
   'mindiff': 0.001600000003236346},
  415.7826: {'row': 8,
   'col': 1,
   'salary': 76503.0,
   'mindiff': 0.9983999999967637},
  315.962: {'row': 4,
   'col': 0,
   'salary': 58137.0,
   'mindiff': 0.008000000001629815},
  310.0489: {'row': 3,
   'col': 2,
   'salary': 57049.0,
   'mindiff': 0.0023999999975785613},
  274.875: {'row': 2, 'col': 0, 'salary': 50577.0, 'mindiff': 0.0},
  295.413: {'row': 3,
   'col': 0,
   'salary': 54356.0,
   'mindiff': 0.008000000001629815},
  289.5217: {'row': 2,
   'col': 2,
   'salary': 53272.0,
   'mindiff': 0.0072000000000116415},
  284.0109: {'row': 2,
   'col': 1,
   'salary': 52258.0,
   'mindiff': 0.005599999996775296},
  254.337: {'row': 1,
   'col': 0,
   'salary': 46798.0,
   'mindiff': 0.008000000001629815},
  268.9783: {'row': 1,
   'col': 2,
   'salary': 49492.0,
   'mindiff': 0.0072000000000116415},
  428.7391: {'row': 8,
   'col': 5,
   'salary': 78888.0,
   'mindiff': 0.005600000004051253},
  248.6685: {'row': 0,
   'col': 2,
   'salary': 45755.0,
   'mindiff': 0.004000000000814907},
  234.0163: {'row': 0,
   'col': 0,
   'salary': 43060.0,
   'mindiff': 1.0008000000016182},
  296.9728: {'row': 2,
   'col': 5,
   'salary': 54643.0,
   'mindiff': 0.004799999995157123}},
 '2019-2020': {421.2772: {'row': 8,
   'col': 2,
   'salary': 77515,
   'mindiff': 0.004799999995157123},
  447.212: {'row': 9,
   'col': 0,
   'salary': 82287,
   'mindiff': 0.008000000001629815},
  463.337: {'row': 9,
   'col': 2,
   'salary': 85254,
   'mindiff': 0.008000000001629815},
  392.2337: {'row': 7,
   'col': 2,
   'salary': 72171,
   'mindiff': 0.0007999999943422154},
  469.7011: {'row': 9,
   'col': 4,
   'salary': 86425,
   'mindiff': 0.0023999999975785613},
  467.2772: {'row': 9,
   'col': 3,
   'salary': 85979,
   'mindiff': 0.004799999995157123},
  377.5924: {'row': 7,
   'col': 0,
   'salary': 69477,
   'mindiff': 0.001600000003236346},
  351.1522: {'row': 5,
   'col': 2,
   'salary': 64612,
   'mindiff': 0.004799999995157123},
  457.2826: {'row': 9,
   'col': 1,
   'salary': 84140,
   'mindiff': 0.001600000003236346},
  371.6848: {'row': 6,
   'col': 2,
   'salary': 68390,
   'mindiff': 0.003200000006472692},
  471.538: {'row': 9,
   'col': 5,
   'salary': 86763,
   'mindiff': 0.008000000001629815},
  357.0435: {'row': 6,
   'col': 0,
   'salary': 65696,
   'mindiff': 0.004000000000814907},
  406.6413: {'row': 8,
   'col': 0,
   'salary': 74822,
   'mindiff': 0.0007999999943422154},
  336.5: {'row': 5, 'col': 0, 'salary': 61916, 'mindiff': 0.0},
  330.6141: {'row': 4,
   'col': 2,
   'salary': 60833,
   'mindiff': 0.005599999996775296},
  315.962: {'row': 4,
   'col': 0,
   'salary': 58137,
   'mindiff': 0.008000000001629815},
  467.2777: {'row': 9,
   'col': 3,
   'salary': 85979,
   'mindiff': 0.09679999999934807},
  469.701: {'row': 9,
   'col': 4,
   'salary': 86425,
   'mindiff': 0.01600000000325963},
  351.1521: {'row': 5,
   'col': 2,
   'salary': 64612,
   'mindiff': 0.01359999999840511},
  254.337: {'row': 1,
   'col': 0,
   'salary': 46798,
   'mindiff': 0.008000000001629815},
  248.6685: {'row': 0,
   'col': 2,
   'salary': 45755,
   'mindiff': 0.004000000000814907},
  310.0489: {'row': 3,
   'col': 2,
   'salary': 57049,
   'mindiff': 0.0023999999975785613},
  274.875: {'row': 2, 'col': 0, 'salary': 50577, 'mindiff': 0.0},
  304.5489: {'row': 3,
   'col': 1,
   'salary': 56037,
   'mindiff': 0.0023999999975785613},
  295.413: {'row': 3,
   'col': 0,
   'salary': 54356,
   'mindiff': 0.008000000001629815},
  325.0924: {'row': 4,
   'col': 1,
   'salary': 59817,
   'mindiff': 0.001600000003236346},
  289.5217: {'row': 2,
   'col': 2,
   'salary': 53272,
   'mindiff': 0.0072000000000116415},
  268.9783: {'row': 1,
   'col': 2,
   'salary': 49492,
   'mindiff': 0.0072000000000116415},
  427.0707: {'row': 8,
   'col': 4,
   'salary': 78581,
   'mindiff': 0.00879999999597203}}}