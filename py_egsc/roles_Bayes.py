from datetime import datetime, timedelta, date
from pay_check import Pay_check, Check_lineitem
from forecast import *
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
        self.retirement_school_year = None                     #may retire in this school year
        self.retirement_probability = None                     #probability of retiring in this school year
        self.empirical_priors = {}                             #priors for steps and/or job titles
        self.fte_empirical_priors = {}    
        return
    
    def get_retirement_school_year(self):
        return(self.retirement_school_year)
    
    def set_retirement_school_year(self,syear):
        self.retirement_school_year = syear
        return
    
    def get_retirement_probability(self):
        return(self.retirement_probability)
    
    def set_retirement_probability(self,prob):
        self.retirement_probability = prob
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
    
    def compute_forecast(self,parm):                           #compute forecast placeholder
        return
    
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
        #self.rate_lookup['2020-2021'] = {}
            
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
    
    def get_cba_salary(self,stepcode):             #step code format is 'yyyy-yyyy-col-step'
        syear = stepcode[:9]
        w = stepcode[10:].split('-')
        col = self.reverse_col_names[w[0]]
        row = int(w[1])-1
        sal = self.cba[syear][row,col]
        return(sal)
    
    def get_next_salary_step(self,stepcode):             #step code format is 'yyyy-yyyy-col-step'
        syear = stepcode[:9]
        y2 = syear[5:]
        y2a = str(int(y2)+1)
        syear = y2 + '-' + y2a
        w = stepcode[10:].split('-')
        newcode=syear + '-' + w[0] + '-'
        row = int(w[1]) + 1 
        if (row >= 10):
            row = 10
        newcode += str(row)
        return(newcode)
    
    def get_step_salary(self,stepcode):    
        syear = stepcode[:9]
        w = stepcode[10:].split('-')
        col = self.reverse_col_names[w[0]]
        row = int(w[1])-1
        sal = self.cba[syear][row,col]
        return(sal)
     
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
        if (('51110' in ftekey) | ('51132' in ftekey)):
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
        strate           = str(rate)
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
        
        error_tolerance  = 3
        
        lineitem.set_payment_type("Other or unknown")
        
        if ((rate > 29.9999) & (rate < 30.0001)):                       #detention coverage
            hours = round(earnings/rate,2)
            lineitem.update_stepinfo('hours',hours)
            if (obj in ['51110','51339','21010']):
                lineitem.set_payment_type("Coverage - other")
                        
        if ((rate > 37.9999) & (rate < 38.0001)):                       #detention coverage
            hours = round(earnings/rate,2)
            lineitem.update_stepinfo('hours',hours)
            if ((obj == '51110') | (obj =='51339')):
                lineitem.set_payment_type("Coverage - other")
        
        if (obj == '51323'):                       #detention coverage

            if (rate > 0.0):
                hours = round(earnings/rate,2)
                lineitem.update_stepinfo('hours',hours)
            lineitem.set_payment_type("Detention coverage")
        
        elif (obj == '51327'):                       #other additional compensation

            if (rate > 0.0):
                hours = round(earnings/rate,2)  
                lineitem.update_stepinfo('hours',hours)
                lineitem.set_payment_type("Other additional compensation")
                
        elif (obj == '51328'):                       #early retirement incentive

            lineitem.set_payment_type("Early Retirement Incentive")
                            
        elif (obj == '51336'):                    

            lineitem.set_payment_type("Class Overage/Weighting")
            
        elif (obj == '51338'):                      
            if (rate > 0.0):
                hours = round(earnings/rate,2)
                lineitem.update_stepinfo('hours',hours)
                lineitem.set_payment_type("Summer Pay")
            
        elif (obj == '51401'):                       #health and medical

            lineitem.set_payment_type("Stipend - other")
            
        elif (obj == '51404'):                       #health and medical

            lineitem.set_payment_type("Stipend - Coaches/Advisors")
                        
        elif (obj == '51406'):                       #health and medical

            lineitem.set_payment_type("Stipend - Athletic Officials")
            
        elif (obj == '51407'):                       #health and medical

            lineitem.set_payment_type("Stipend - mentors")
            
        elif (obj == '52121'):                       #health and medical

            lineitem.set_payment_type("Health and Medical")
            
        elif (obj == '53214'):                       #health and medical

            lineitem.set_payment_type("Mentoring")
                        
        elif (obj == '53301'):                       #health and medical

            lineitem.set_payment_type("Professional Development and Training")
            
                                    
        elif (obj == '53416'):                       #health and medical

            lineitem.set_payment_type("Officials/Referees")

        
        elif strate in rate_lookup[school_year].keys():
            
            lineitem.set_payment_type("Contract salary")
            
            col = rate_lookup[school_year][strate]['col']
            self.update_priors('col',col,ppo)
            
            row = rate_lookup[school_year][strate]['row']
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
                            lineitem.update_stepinfo('from_prior',False)
                       
                            within_error_tolerance = True
                        
        else:                                    #fill in from 51110 priors if possible
            priors = ppo.get_priors()
            fte_priors = ppo.get_fte_priors()

            col = None
            for i in priors['col'].keys():
                if (priors['col'][i] > 0.9):
                    col = i

            row = None
            for i in priors['row'].keys():
                if (priors['row'][i] > 0.9):
                    row = i
              
            payments = None
            for i in priors['payments'].keys():
                if (priors['payments'][i] > 0.9):
                    payments = i
                            
            ftes = {}
            try:
                for ftk in fte_priors.keys():
                    maxftk = 0.0
                    try:
                        for i in fte_priors[ftk].keys():
                            if (fte_priors[ftk][i] > maxftk):
                                maxftk = fte_priors[ftk][i]
                        ftes[ftk] = round(maxftk,4)
                    except TypeError:
                        print('TypeError',ftk,maxftk,fte_priors[ftk][i])
            except KeyError:
                  print('decode earnings from priors',ftekey,ftepriors)
                      
            if ((col is not None) & (row is not None)):
                lineitem.update_stepinfo('step',school_year + '-' + self.col_names[col] + \
                    '-' + str(row+1))        #code is:  yyyy-yyyy-cat-step
                lineitem.update_stepinfo('salary',self.cba[school_year][row][col])
            if (payments is not None):
                lineitem.update_stepinfo('payments',self.n_payments[payments])
            if (ftes is not None):
                lineitem.update_stepinfo('ftes',ftes)
            lineitem.update_stepinfo('from_prior',True)
            #lineitem.set_payment_type('Other or unknown')
            
        return
    
    def compute_forecast(self,parm):                        #compute next forecast one payperiod beyond this one
        role    = parm['role']
        fc_in   = parm['forecast']
        if (fc_in.get_payment_type() == 'Contract salary'):   #contract salary forecast
            fc = fc_in.make_copy()                            #deepcopy to create new forecast
            fc.update_school_year()                           #advance school_year and school_year_seq
            stepinfo = fc.get_stepinfo()                      #update stepinfo
            stepcode = stepinfo['step']                       #get step code 'yyyy-yyyy-col-step'
            if (fc_in.school_year != fc.school_year):         #update step if new school year
                stepcode = self.get_next_salary_step(stepcode) #get step for next payperiod
                stepinfo['step'] = stepcode                    #update stepcode in stepinfo
            sal = self.get_cba_salary(stepcode)                #compute salary in next payperiod 
            sal = round(sal,2)
            fte = stepinfo['fte']                             #assume fte is the same
            payments = stepinfo['payments']                   #assume number of payments is the same
            amt = round(fte*sal/payments,2)                   #new earnings amount
            fc.amt = amt                                      #update forecast object
            stepinfo['salary'] = sal                          #update salary in stepinfo
            fc.set_stepinfo(stepinfo)                         #put new stepinfo in forecast
            return(fc)                                        #return new forecast
        else:
            return
        
class Para(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name) 
        
        #empirical priors
        self.empirical_priors = {0: {0: 0.020313942751615882, 1: 0.029085872576177285, 2: 0.041089566020313946, 
                3: 0.050784856879039705, 4: 0.04016620498614958, 5: 0.012003693444136657, 6: 0.8065558633425669},
         1: {0: 0.015625, 1: 0.00390625, 2: 0.00390625, 3: 0.10546875, 4: 0.203125, 5: 0.0078125, 6: 0.66015625},
         2: {0: 0.03303883673845021, 1: 0.04638321369409166, 2: 0.04831584759801215, 3: 0.04233388551444874,
                4: 0.036628013988588254, 5: 0.03285477636664826, 6: 0.7604454260997607}}

        self.cba = {
                'Para':{
                    '2013-2014':{7:18.04, 6:17.02, 5:16.18, 4:15.73, 3:15.26, 2:14.93, 1:14.46},
                    '2014-2015':{7:18.40, 6:17.36, 5:16.50, 4:16.04, 3:15.57, 2:15.23, 1:14.75},
                    '2015-2016':{7:18.77, 6:17.71, 5:16.83, 4:16.37, 3:15.88, 2:15.53, 1:15.04},
                    '2016-2017':{7:19.14, 6:18.06, 5:17.17, 4:16.69, 3:16.19, 2:15.84, 1:15.35},
                    '2017-2018':{7:19.14, 6:18.06, 5:17.17, 4:16.69, 3:16.19, 2:15.84, 1:15.35},
                    '2018-2019':{7:19.52, 6:18.42, 5:17.51, 4:17.02, 3:16.51, 2:16.16, 1:15.66},
                    '2019-2020':{7:19.91, 6:18.79, 5:17.86, 4:17.36, 3:16.84, 2:16.48, 1:15.97},
                    '2020-2021':{7:19.91, 6:18.79, 5:17.86, 4:17.36, 3:16.84, 2:16.48, 1:15.97}
                },
                'Office':{
                    '2013-2014':{7:21.51, 6:20.15, 5:19.19, 4:18.25, 3:17.27, 2:16.59, 1:16.11},
                    '2014-2015':{7:21.94, 6:20.15, 5:19.19, 4:18.25, 3:17.27, 2:16.59, 1:16.11},
                    '2015-2016':{7:22.38, 6:20.55, 5:19.58, 4:18.62, 3:17.62, 2:16.92, 1:16.43},
                    '2016-2017':{7:22.83, 6:20.96, 5:19.97, 4:18.99, 3:17.97, 2:17.26, 1:16.76},
                    '2017-2018':{7:22.83, 6:20.96, 5:19.97, 4:18.99, 3:17.97, 2:17.26, 1:16.76},
                    '2018-2019':{7:23.29, 6:21.38, 5:20.37, 4:19.37, 3:18.33, 2:17.61, 1:17.10},
                    '2019-2020':{7:23.76, 6:21.81, 5:20.78, 4:19.76, 3:18.70, 2:17.96, 1:17.44},
                    '2020-2021':{7:23.76, 6:21.81, 5:20.78, 4:19.76, 3:18.70, 2:17.96, 1:17.44}
                },
                'Central':{
                    '2013-2014':{7:25.57, 6:23.67, 5:22.70, 4:21.77, 3:20.80, 2:20.12, 1:19.64},
                    '2014-2015':{7:25.57, 6:23.67, 5:22.70, 4:21.77, 3:20.80, 2:20.12, 1:19.64},
                    '2015-2016':{7:26.08, 6:24.15, 5:23.16, 4:22.21, 3:21.22, 2:20.52, 1:20.03},
                    '2016-2017':{7:26.60, 6:24.63, 5:23.62, 4:22.65, 3:21.64, 2:20.93, 1:20.43},
                    '2017-2018':{7:26.60, 6:24.63, 5:23.62, 4:22.65, 3:21.64, 2:20.93, 1:20.43},
                    '2018-2019':{7:27.13, 6:25.12, 5:24.09, 4:23.10, 3:22.07, 2:21.35, 1:20.84},
                    '2019-2020':{7:27.67, 6:25.63, 5:24.57, 4:23.57, 3:22.51, 2:21.78, 1:21.26},
                    '2020-2021':{7:27.67, 6:25.63, 5:24.57, 4:23.57, 3:22.51, 2:21.78, 1:21.26}
                }
        }
        
        self.jobs = {0:'Para',1:'Office',2:'Central'}
        self.job_code = {'Para':0,'Office':1,'Central':2}
        #with open('../../finance_subcommittee/para_rate_lookup_1_18_2021.pkl', 'rb') as handle:
        #    self.para_rate_lookup =  pickle.load(handle)
            
        return
    
    def update_cba(self,base_year,new_year,para,office,central):
        factors = [para,office,central]
        self.cba[new_year] = {}
        for j in self.jobs.keys():
            self.cba[self.jobs[j]][new_year] = {}
            for k in self.cba[self.jobs[j]][base_year].keys():
                self.cba[self.jobs[j]][new_year][k] = round(self.cba[self.jobs[j]][base_year][k]*factors[j],4)
        return
    
    def get_cba(self):
        return(self.cba)

    def get_rate(self,job,step):
        step_number = int(step[len(step)-1])
        school_year = step[:9]
        try:
            rate = self.cba[job][school_year][step_number]
        except KeyError:
            print('No rate for ',job,step)
            return
        return(rate)
        
    
    def get_future_step(self,current_step,years_ahead):
        words = current_step.split('-')
        year1 = int(words[0]) + years_ahead
        newstep = str(year1) + '-' + str(year1 + 1) + '-' + str(min(7,int(words[2])+years_ahead))
        return(newstep)
    
    def get_job_code(self,job):
        try:
            return(self.job_codes[job])
        except KeyError:
            print('No code for job ',job)
            return
    
    def get_para_rate_lookup(self):
        return(self.para_rate_lookup)
    
    def set_empirical_priors(self,prior):
        try:
            self.empirical_priors = cp.deepcopy(prior)
        except KeyError:
            print('Para - set empirical priors KeyError ',prior)
        return
        
    def update_priors(self,job,n,ppo):
        """update_priors(param,value) updates the priors for param given value"""
        try:
            job_code = self.job_code[job]
        except KeyError:
            print('Para - update priors - job code lookup error',job,n)
            return
        try:
            for i in ppo.priors[job_code].keys():
                ppo.priors[job_code][i] = 0.5*ppo.priors[job][i]
        except KeyError:
            print('Para - update_priors KeyError ',job,job_code,n,ppo.priors)
            return
        try:
            ppo.priors[job_code][n] += 0.5
        except KeyError:
            print('Para - update observed prior KeyError ',param,n,ppo.priors)
        return
        
    #get step, hours for paras, office, and central office
    
    def decode_earnings(self,lineitem):
       
        fund             = lineitem.get_fund()
        obj              = lineitem.get_obj()
        rate             = lineitem.get_rate()
        acct             = lineitem.get_acct()
        earnings         = lineitem.get_earnings()
        chk              = lineitem.get_parent_check()      #parent check object
        ppo              = chk.get_parent_payperiod()       #parent payperiod object
        school_year      = ppo.get_school_year()            #school year for current lineitem
        syseq            = ppo.get_school_year_seq()        #school year sequence number
        parent_role      = ppo.get_parent_role()            #get parent role
        role_name        = parent_role.get_role_name()
        person           = self.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        payment_type     = 'Other or unknown'
        
        rate_error_tolerance  = 0.02
        
        if rate > 0.0:
                     
            if ('PARA' in role_name):
                jobs = ('Para',)
            elif ('SECRET' in role_name):
                jobs = ('Office','Central')
            
            min_job  = None
            min_diff = 1000.
            min_step = None
                     
            for job in jobs:
                for step in self.cba[job][school_year].keys():
                    diff = abs(self.cba[job][school_year][step] - rate)
                    if (diff < min_diff):
                        min_diff = diff
                        min_job  = job
                        min_step = step
                     
            if (min_diff < rate_error_tolerance):
                stepcode = school_year + '-' + str(min_step)         
                hours = None
                if (abs(rate)>0.0):            
                    hours = earnings/rate
                lineitem.set_payment_type("Contract salary")
                self.update_priors(job,step,ppo)
                lineitem.update_stepinfo('step',stepcode)        #code is:  yyyy-yyyy-step
                lineitem.update_stepinfo('hours',hours)    
                lineitem.update_stepinfo('mindiff',min_diff)
                lineitem.update_stepinfo('MUNIS_rate',rate)
                lineitem.update_stepinfo('table_job',min_job)
                lineitem.update_stepinfo('from_prior',False)
            
            else:
                max_job = None
                max_step = None
                priors = ppo.get_priors()
            
                for job in priors.keys():
                    for i in priors[job].keys():
                        prob = priors[job][i]
                        if (prob > 0.9):
                            max_job = job
                            max_step = i
                if (max_job is not None):
                    step = i+1
                    jobname = self.jobs[max_job]
                    rate = self.cba[jobname][school_year][i+1]
                    hours = None
                    if (rate > 0.0):
                        hours = earnings/rate
                    lineitem.update_stepinfo('step',school_year + '-' + str(step))   #code is:  yyyy-yyyy-step
                    lineitem.update_stepinfo('hours',hours)    
                    lineitem.update_stepinfo('MUNIS_rate',rate)
                    lineitem.update_stepinfo('table_job',jobname)
                    lineitem.update_stepinfo('from_prior',True)
        return
        
class Office(Para):
    
    def __init__(self, person, role_name):
        Para.__init__(self, person, role_name)
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
                
        self.empirical_priors     = {0:1/6., 1:1/6., 2:1/6., 3:1/6., 4:1/6., 5:1/6.}
        
        self.fte_empirical_priors = {}
        
        self.cba = {
            'Custodian':{
                '2014': {'2014-0': 12.48, '2014-1': 14.22, '2014-2': 14.99,
                              '2014-3': 15.77, '2014-4': 16.54, '2014-5': 17.83},
                '2015': {'2015-0': 12.73, '2015-1': 14.50, '2015-2': 15.29,
                              '2015-3': 16.09, '2015-4': 16.87, '2015-5': 18.19},
                '2016': {'2016-0': 13.24, '2016-5': 18.5500},
                '2017': {'2017-0': 13.6364, '2017-5': 18.9249},
                '2018': {'2018-0': 14.0455, '2018-5': 19.3034},
                '2019': {'2019-0': 14.4300, '2019-5': 19.3034},
                '2020': {'2020-0': 14.4300, '2020-5': 19.6900},
                '2021': {'2021-0': 14.8300, '2021-5': 20.0800}
                },
            'Maintenance':{
                '2014': {'2014-1': 15.00, '2014-2': 15.61, '2014-3':16.24,
                              '2014-4': 16.86, '2014-5': 18.00},
                '2015': {'2015-1': 15.30, '2015-2': 15.92, '2015-3':16.56,
                              '2015-4': 17.20, '2015-5': 18.36},
                '2016': {'2016-1': 18.7300},
                '2017': {'2017-1': 19.1017},
                '2018': {'2018-1': 19.4837},
                '2019': {'2019-1': 19.8700},
                '2020': {'2020-1': 19.8700},
                '2021': {'2021-1': 20.2710}
                },
            'Electrician':{
                '2014': {'2014-1': 21.09, '2014-2': 22.20, '2014-3': 23.30,
                              '2014-4': 24.42, '2014-5': 25.52},
                '2015': {'2015-1': 21.51, '2015-2': 22.64, '2015-3': 23.77, 
                              '2015-4': 24.91, '2015-5': 26.03},
                '2016': {'2016-1': 26.5506},
                '2017': {'2017-1': 27.0816},
                '2018': {'2018-1': 27.6232},
                '2019': {'2019-1': 27.6232},
                '2020': {'2020-1': 28.1762},
                '2021': {'2021-1': 28.7397}
                },
            'Maint Dir':  {
                '2014': {'2014-1': 27.7134},
                '2015': {'2015-1': 27.7134},
                '2016': {'2016-1': 28.4062},
                '2017': {'2017-1': 28.9743},
                '2018': {'2018-1': 29.5500},
                '2019': {'2019-1': 29.5500},
                '2020': {'2020-1': 30.6000},
                '2021': {'2021-1': 30.6000}
                },
            'Facility Dir': {
                '2014': {'2014-1': 33.3189},
                '2015': {'2015-1': 33.9853},
                '2016': {'2016-1': 34.8350},
                '2017': {'2017-1': 35.1833},
                '2018': {'2018-1': 35.8869},
                '2019': {'2019-1': 36.6046},
                '2020': {'2020-1': 36.6046},
                '2021': {'2021-1': 37.3368}
                },
            'Custodian PT':  {
                '2014': {'2014-1': 10.0000},
                '2015': {'2015-1': 10.0000},
                '2016': {'2016-1': 10.0000},
                '2017': {'2017-1': 10.0000,'2017-2': 10.1000},
                '2018': {'2018-1': 10.0000,'2018-2': 10.1000},
                '2019': {'2019-1': 14.0500},
                '2020': {'2020-1': 14.0500},
                '2021': {'2021-1': 14.0500}
                }
            }
        
        self.roles = {'CUSTODIAN': 'Custodian', 'CUST PT': 'Custodian PT', 
                      "CUST>'09": 'Custodian',"MAINT>'07": 'Maintenance', "CUST<'09": 'Custodian',
                      'DIR MAINT': 'Maint Dir', 'ELECTRICAN': 'Electrician', 
                      'MAINTENANC': 'Maintenance', 'FACILTY DR': 'Facility Dir'}
        
        self.prior_jobs = {0:'Custodian',1:'Maintenance',2:'Electrician',
                           3:'Maint Dir',4:'Facility Dir',5:'Custodian PT'}
        
        self.role_codes = {'CUSTODIAN':0, 'MAINTENANC':1, 'ELECTRICAN':2, 'DIR MAINT':3, 
                         'FACILTY DR':4, 'CUST PT':5, "CUST>'09":0, "CUST<'09": 0, "MAINT>'07":1}
        
        self.jobs_prior = {'Custodian':0, 'Maintenance':1, 'Electrician':2,
                           'Maint Dir':3, 'Facility Dir':4, 'Custodian PT':5}
           
        self.stipend = {
            '2014': {
                        #"Facilities stipend":                          650.00,   no general stipend this year
                        "Head custodian stipend - Elementary":        1154.84,
                        "Head custodian stipend - Middle School":     1231.83,
                        "Head custodian stipend - High School":       2001.73,
                        "Maintenance Foreman stipend":                2466.56,
                        },
            '2015': {
                        #"Facilities stipend":                         650.00,
                        "Head custodian stipend - Elementary":        1177.94,
                        "Head custodian stipend - Middle School":     1256.47,
                        "Head custodian stipend - High School":       2041.76,
                        "Maintenance Foreman stipend":                2515.89
                        },
            '2016': {
                        #"Facilities stipend":                          650.00,
                        "Head custodian stipend - Elementary":        1300.00,
                        "Head custodian stipend - Middle School":     1500.00,
                        "Head custodian stipend - High School":       2200.00,
                        "Maintenance Foreman stipend":                2700.00,
                        },
            '2017': {
                        #"Facilities stipend":                          650.00,
                        "Head custodian stipend - Elementary":        1300.00,
                        "Head custodian stipend - Middle School":     1500.00,
                        "Head custodian stipend - High School":       2200.00,
                        "Maintenance Foreman stipend":                2700.00,
                        },
            '2018': {
                        "Facilities stipend":                          650.00,   #just in case
                        "Head custodian stipend - Elementary":        1300.00,
                        "Head custodian stipend - Middle School":     1500.00,
                        "Head custodian stipend - High School":       2200.00,
                        "Maintenance Foreman stipend":                2700.00,
                        },
            '2019': {
                        "Facilities stipend":                          650.00,
                        "Head custodian stipend - Elementary":        1300.00,
                        "Head custodian stipend - Middle School":     1500.00,
                        "Head custodian stipend - High School":       2200.00,
                        "Maintenance Foreman stipend":                2700.00,
                        },
            '2020': {
                        "Facilities stipend":                          650.00,
                        "Head custodian stipend - Elementary":        1300.00,
                        "Head custodian stipend - Middle School":     1500.00,
                        "Head custodian stipend - High School":       2200.00,
                        "Maintenance Foreman stipend":                2700.00,
                        },
            '2021': {
                        "Facilities stipend":                          650.00,
                        "Head custodian stipend - Elementary":        1300.00,
                        "Head custodian stipend - Middle School":     1500.00,
                        "Head custodian stipend - High School":       2200.00,
                        "Maintenance Foreman stipend":                2700.00,
                        }
                }
        return
        
    def get_cba_matrix(self):
        return(self.cba)
    
    def get_cba_steps(self):
        return(self.cba_steps)
    
    def get_stipend(self):
        return(self.stipend)
    
    def get_rate_lookup(self):
        """Null get_rate_lookup function for facilities"""
        return
    
    def get_cba_matrix_by_year(self, school_year):
        return(self.cba[school_year])     
        
    def xset_default_priors(self, priors=None):
        if (priors is None):
            self.default_priors['job'] = self.set_uniform_priors(4)
        else:
            self.default_priors = priors
            
    def get_empirical_priors(self):
        return(self.empirical_priors)
    
    def decode_earnings(self,lineitem):
       
        fund             = lineitem.get_fund()
        obj              = lineitem.get_obj()
        rate             = lineitem.get_rate()
        acct             = lineitem.get_acct()
        earnings         = lineitem.get_earnings()
        
        chk              = lineitem.get_parent_check()      #parent check object
        ppo              = chk.get_parent_payperiod()       #parent payperiod object
        school_year      = ppo.get_school_year()            #school year for current lineitem
        fiscal_year      = str(ppo.get_fiscal_year())       #fiscal year for current lineitem
        fyseq            = ppo.get_fiscal_year_seq()        #fiscal year sequence number
        parent_role      = ppo.get_parent_role()            #get parent role
        role_name        = parent_role.get_role_name()
        rate_lookup      = self.get_rate_lookup()
        person           = self.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        payment_type     = 'Other or unknown'
        
        error_tolerance  = 3
        rate_tolerance   = 0.03
        
        mindiff = 1000.0                                   #look up salary in cba table
        min_syr = None
        min_job = None
        min_OT  = None
        
        if (rate > 0.0):
            hours = round(earnings/rate,2)
        else:
            hours = None
            
        jobname = self.roles[role_name]
        cbat = self.cba[jobname]                                   
        for fyr in cbat.keys():
            for step in cbat[fyr].keys():
                for fact in [1.0,1.5]:
                    diff = abs(rate - fact*cbat[fyr][step])
                    if (diff < mindiff):
                        mindiff = diff
                        min_fyr = fyr
                        min_job = jobname
                        min_step = step
                        min_fact = fact
                        
             
                
        if (mindiff < rate_tolerance):
            lineitem.update_stepinfo('MUNIS_rate',cbat[min_fyr][min_step]) 
            cba_step_number = min_step[5:]
            if ((fiscal_year > '2015') & (jobname != 'Custodian')):
                cba_step_number = '1'
            elif (cba_step_number == '2'):
                cba_step_number = '0'
            cba_step = fiscal_year + '-' + cba_step_number
            lineitem.update_stepinfo('cba_rate',cbat[fiscal_year][cba_step]) 
            lineitem.update_stepinfo('cba_step', cba_step)
            lineitem.update_stepinfo('hours',hours)    
            lineitem.update_stepinfo('mindiff',round(mindiff,4))
            lineitem.update_stepinfo('job',min_job)
            lineitem.update_stepinfo('step',min_step)
            
            lineitem.update_stepinfo('from_priors',False)
            if (min_fact == 1.0):
                lineitem.set_payment_type("Contract salary")
                lineitem.update_stepinfo('OT',False)
            else:
                lineitem.set_payment_type("Overtime")
                lineitem.update_stepinfo('OT',True)
            self.update_priors(min_job,ppo)
            return
        
        else:   
            mindiff   = 1000.0                                     #check stipends
            min_ptype = None
            min_fact  = None
            
            for fyear in self.stipend.keys():                      #search through stipend table by year
                cbas = self.stipend[fyear]                         #stipend for this fiscal year
                for ptype in cbas.keys():                          #search through person types in table
                    for fact in [1.0,1.5]:                         #try straight time and time-and-a-half rates
                        sp = fact*cbas[ptype]                      #factor times stipend 
                        if (rate > 0.0):                           #if rate is not zero, use it to check
                            diff = abs(80.0*26.0*rate - sp)        #stipend - 80*26*hourly_rate
                            if (diff < mindiff):                   #is this the best fit so far?
                                mindiff = diff                     #if so, save the difference, ptype, and fact
                                min_ptype = ptype
                                min_fact = fact
                            diff = abs(26.0*rate - sp)             #another possibility to check - is it payperiod rate?
                            if (diff < mindiff):                   #is this the best fit yet?
                                mindiff = diff                     #if so save diff, ptype, fact
                                min_ptype = ptype
                                min_fact = fact
                        else:                                      #if rate=0.0, try using earnings
                            diff = abs(earnings*26.0*80.0 - sp)   #I think this should be earnings*26.0!!!!
                            #diff = abs(earnings*26.0 - sp)         #changed 3/3/2021
                            if (diff < mindiff):                   #is this the best so far?
                                mindiff = diff                     #if so save diff, ptype, fact
                                min_ptype = ptype
                                min_fact = fact
                            diff = abs(earnings - sp)              #another possibility - earnings is whole stipend
                            if (diff < mindiff):                   #is this the best fit so far?
                                mindiff = diff                     #if so save diff, ptype, fact
                                min_ptype = ptype
                                min_fact = fact
                                
            if (mindiff < error_tolerance):                       #did we find an acceptably close fit?
                if (min_fact == 1.5):
                    min_ptype = min_ptype + ' - OT'
                lineitem.set_payment_type(min_ptype)
                return
            
            elif ((rate == 0.0) & (obj == '20430')):
                lineitem.set_payment_type("Obj 20430") 
                return  
            
            elif (chk.get_date() == date(2018,1,5)):    # mysterious 1/5/2018 payments
                lineitem.set_payment_type("Mysterious 1/5/2018") 
                return  
            
            else:
                lineitem.set_payment_type("Other or unknown") 
                return
        return
    
                
    def update_priors(self,jobname,ppo):
        """update_priors(param,value) updates the priors for param given value"""
            
        try:
            n = self.jobs_prior[jobname]
        except KeyError:
            print('Facilities - jobname key error: ',jobname)
            
        try:
            for i in ppo.priors.keys():
                ppo.priors[i] = 0.5*ppo.priors[i]
        except KeyError:
            print('Facilities - update_priors KeyError ',n,ppo.priors)
            return
        try:
            ppo.priors[n] += 0.5
        except KeyError:
            print('Facilities - update_priors KeyError ',n,ppo.priors)
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
        
class Custodian_PT(Facilities):
    
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

        person           = self.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        
        lineitem.set_payment_type("Other or unknown")
            
        if (obj in ['51110','51115','21010']):    
            if (isinstance(parent_role,Substitute_teacher)):
                if (str(rate) in ['75.0','125.0']):
                    days = earnings/rate
                    lineitem.update_stepinfo('cba_rate',rate) 
                    lineitem.update_stepinfo('days',days)
                    lineitem.set_payment_type("Contract salary")
                    if (str(rate) == '75.0'):
                        lineitem.update_stepinfo('role',"Substitute teacher")
                    elif (str(rate) == '125.0'):
                        lineitem.update_stepinfo('role',"Substitute nurse")
                if (str(rate) in ['30.0']):
                    hours = earnings/rate
                    lineitem.update_stepinfo('cba_rate',rate) 
                    lineitem.update_stepinfo('hours',hours)
                    if (isinstance(parent_role,Substitute_teacher)):
                        lineitem.update_stepinfo('role',"Substitute teacher")
                    if (isinstance(parent_role,Substitute_para)):
                        lineitem.update_stepinfo('role',"Substitute para")
                        
            elif (isinstance(parent_role,Substitute_para)):
                if (str(rate) in ['10.0','10.1','10.4']):
                    hours = earnings/rate
                    lineitem.update_stepinfo('cba_rate',rate) 
                    lineitem.update_stepinfo('hours',hours) 
                    lineitem.update_stepinfo('role',"Substitute para")
                    lineitem.set_payment_type("Contract salary") 
        elif (obj == '52121'):                       #health and medical
            lineitem.set_payment_type("Health and Medical")
        return
        
class Substitute_teacher(Substitutes):
    
    def __init__(self, person, role_name):
        Substitutes.__init__(self, person, role_name) 
        return
        
class Substitute_para(Substitutes):
    
    def __init__(self, person, role_name):
        Substitutes.__init__(self, person, role_name)
        return
        
class Appendix_B(Role):
    
    def __init__(self, person, role_name):
        Role.__init__(self, person, role_name)
        
        self.schedule_B = {
            '2013-2014' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2014-2015' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2015-2016' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2016-2017' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2017-2018' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2018-2019' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2019-2020' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2020-2021' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496},
            '2021-2022' :
                {1:19306., 2:21123., 3:22941., 4:24758., 5:26576., 6:28393., 7:30211., 8:32028.,9:33846., 10:39496}
        }
        
        self.stipend_lookup = {}
        
        for syear in self.schedule_B.keys():
            if syear not in self.stipend_lookup.keys():
                self.stipend_lookup[syear] = {}
            for pts in np.arange(6,13):
                for step in self.schedule_B[syear].keys():
                    for frac in [1.0,0.6]:
                        stipend = 0.01*frac*pts*self.schedule_B[syear][step]
                        if (step == 10):
                            if (stipend > 0.0):
                                stipend += 25.
                            if (stipend > 999):
                                stipend += 25.
                            if (stipend > 1999):
                                stipend += 25.
                            if (stipend > 2999):
                                stipend += 25.
                        stipend = round(stipend,2)
                        sstipend = str(stipend)
                        if sstipend not in self.stipend_lookup[syear].keys():
                            self.stipend_lookup[syear][sstipend] = {}
                            self.stipend_lookup[syear][sstipend]['pts'] = pts
                            self.stipend_lookup[syear][sstipend]['step'] = step
                            self.stipend_lookup[syear][sstipend]['frac'] = frac
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
        syear            = ppo.get_school_year()            #school year for current lineitem
        syseq            = ppo.get_school_year_seq()        #school year sequence number
        parent_role      = ppo.get_parent_role()            #get parent role
        person           = self.get_parent_person()  #parent person object
        name             = person.get_name()                #name of person
        
        lineitem.set_payment_type("Other or unknown")
        
        if syear in self.stipend_lookup.keys():
            searnings = str(earnings)
        
            if searnings in self.stipend_lookup[syear].keys():
                lineitem.update_stepinfo('step',self.stipend_lookup[syear][searnings]['step'])
                lineitem.update_stepinfo('pts',self.stipend_lookup[syear][searnings]['pts'])
                lineitem.update_stepinfo('frac',self.stipend_lookup[syear][searnings]['frac'])
                lineitem.set_payment_type("Coach/Advisor stipend")
        return
    
    def get_schedule_B(self):
        return(self.schedule_B)
    
    def get_step_10_increase(self):
        return(self.step_10_increase)
    
    def get_point_values(self):
        return(self.point_values)
        
class Coach(Appendix_B):
    
    def __init__(self, person, role_name):
        Appendix_B.__init__(self, person, role_name)
        
        self.point_values = {}
        for i in np.arange(6,13):
            self.point_values[i] = 0
        return
    
    def get_point_values(self):
        return(self.point_values)
            
class Advisor(Appendix_B):
    
    def __init__(self, person, role_name):
        Appendix_B.__init__(self, person, role_name)
        return