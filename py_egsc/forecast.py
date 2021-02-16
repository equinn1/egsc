from datetime import datetime, timedelta, date
from pay_check import Pay_check, Check_lineitem
import copy as cp
import numpy as np
from numpy.random import choice

class Forecast():                                #class for dates at end of payperiods
    """Provides a forecast object given an arbitrary start date"""
    def __init__(self):                               #constructor
        self.base_school_year     = None
        self.base_school_year_seq = None
        self.school_year          = None              #school year string 'yyyy-yyyy'
        self.school_year_seq      = None              #payperiod number within school year 1-26
        self.payment_type         = None              #payment type
        self.fund                 = None              #accounting - fund  
        self.acct                 = None              #accounting - acct
        self.obj                  = None              #accounting - obj
        self.amt                  = None              #amt
        self.stepinfo             = None              #step info
        self.simplex              = None              #default simplex
        return
    
    def from_Check_lineitem(self,litem,role):
        check                     = litem.get_parent_check()
        pp                        = check.get_parent_payperiod()
        self.base_school_year     = pp.get_school_year()
        self.base_school_year_seq = pp.get_school_year_seq()
        self.school_year          = self.base_school_year
        self.school_year_seq      = self.base_school_year_seq
        self.payment_type         = litem.get_payment_type()
        self.fund                 = litem.get_fund()
        self.acct                 = litem.get_acct()
        self.obj                  = litem.get_obj()
        self.amt                  = litem.get_earnings()
        self.stepinfo             = litem.get_stepinfo()
        self.simplex              = Simplex()
        return
    
    def make_copy(self):
        """Return a deepcopy clone of this forecast"""
        newfc = cp.deepcopy(self)
        return(newfc)
        
        
        
    def get_next_school_year(self,syear):
        """Return the next school year"""
        y1 = int(syear[5:])
        nsyr = str(y1) + '-' + str(y1+1)
        return(nsyr)
    
    def print(self):
        print(self.base_school_year,self.base_school_year_seq,self.school_year,self.school_year_seq, \
            self.payment_type,self.fund,self.acct,self.obj,self.amt,self.stepinfo,self.simplex)
        return
    
    def update_school_year(self):
        """Advance school_year and school_year_seq one payperiod"""
        syear = self.school_year
        if (self.school_year_seq < 26):
            self.school_year = syear
            self.school_year_seq += 1
        else:
            y1 = int(syear[5:])
            self.school_year = str(y1) + '-' + str(y1+1)
            self.school_year_seq = 1
        return
        
    def get_school_year(self):
        return(self.school_year)
    
    def get_base_school_year(self):
        return(self.base_school_year)
    
    def set_base_school_year(self,byear):
        self.base_school_year = byear
        return
    
    def set_school_year(self,syear):
        self.school_year = syear
        return
        
    def get_simplex(self):
        return(self.simplex)
    
    def set_simplex(self,splex):
        self.simplex = splex
        return
    
    def get_stepinfo(self):
        return(self.stepinfo)
    
    def set_stepinfo(self,stepinfo):
        self.stepinfo = stepinfo
        return
              
    def get_payment_type(self):
        return(self.payment_type)
    
    def set_payment_type(self,ptype):
        self.payment_type = ptype
        return
        
    def get_school_year_seq(self):
        return(self.school_year_seq)
    
    def get_base_school_year_seq(self):
        return(self.base_school_year_seq)
    
    def set_base_school_year_seq(self,byseq):
        self.base_school_year_seq = byseq
        return
    
    def set_school_year(self,syseq):
        self.school_year_seq = syseq
        return
    
    def get_fund(self):
        return(self.fund)
    
    def set_fund(self,fund):
        self.fund = fund
        return
        
    def get_amt(self):
        return(self.amt)
    
    def set_fund(self,amt):
        self.amt = amt
        return
        
    def get_acct(self):
        return(self.acct)
    
    def set_acct(self,acct):
        self.acct = acct
        return
        
    def get_obj(self):
        return(self.obj)
    
    def set_school_year(self,obj):
        self.obj = obj
        return
    
    def add_personnel(self,prsnl):
        ix = len(self.personnel)
        self.personnel[ix] = prsnl
        return
    
    def get_personnel(self):
        return(self.personnel)
        
class Simplex():                                                            #generic check class
    def __init__(self,p=1.0,lbl='default',forecast=None):                #constructor
        self.simplex   = {1:{'p':p, 'lbl':lbl, 'forecast':forecast}}
        self.weights = []
        self.amounts = []
        return

    def get_simplex(self):
        return(self.simplex)
    
    def compute_weights(self):
        self.weights = []
        for i in sorted(self.simplex.keys()):
            self.weights.append(self.simplex[i]['p'])
        return
    
    def get_amounts(self):
        self.amounts = []
        for i in sorted(self.simplex.keys()):
            self.amounts.append(self.simplex[i]['forecast'].get_amt())
        return
        
    def get_weighted_sample(self,n):
        samp = []
        for i in np.arange(n):
            samp.append(choice(self.amounts,p=self.weights))
        return(samp)
    
    def get_expected(self):
        ex = 0.0
        for i in np.arange(len(self.weights)):
            ex += self.weights[i] * self.amounts[i]
        return(ex)
    
    def print(self):
        for ix in sorted(self.simplex.keys()):
            print(ix,self.simplex[ix]['p'],self.simplex[ix]['lbl'],self.simplex[ix]['forecast'])
        return
    
    def add_forecast(self,prob,label,forecast):
        ix = len(self.simplex)
        for i in self.simplex.keys:
            self.simplex[i]['p'] = self.simplex[i]['p']*(1.0-prob)
        self.simplex[ix]['p'] = prob
        self.simplex[ix]['lbl'] = label
        self.simplex[ix]['forecast'] = forecast
        return
    
    def set_simplex(self,plex):
        self.simplex = plex
        return
            
    def get_label(self,ix):
        return(self.simplex[ix]['lbl'])
    
    def set_label(self,ix,lbl):
        self.simplex[ix]['lbl'] = lbl
        return
    
    def get_forecast(self,ix):
        return(self.simplex[ix]['forecast'])
    
    def set_forecast(self,ix,forecast):
        self.simplex[ix]['forecast'] = forecast
        return
            
    def get_p(self,ix):
        return(self.simplex[ix]['p'])
    
    def set_p(self,ix,prob):
        self.simplex[ix]['p'] = prob
        for i in self.simplex.keys():
            if (i != ix):
                self.simplex[i]['p'] = self.simplex[i]['p']*(1.0-prob)
        return
      
class Position():                                                            #generic check class
    def __init__(self,fcast,role,fte,start,end=None):                #constructor
        self.parent_forecast  = fcast                         #
        self.role     = role                     #Role object
        self.fte      = fte                      #fte
        self.start    = start
        return

    def get_simplex(self):
        return(self.simplex)
    
    def set_simplex(self,simplex):
        self.simplex = simplex
        return
                
class Personnel():                                                            #generic check class
    def __init__(self,pers,role):                #constructor
        self.person   = pers                     #Person object
        self.role     = role                     #Role object
        self.simplex  = Simplex()                #Simplex object for 
        return

    def get_simplex(self):
        return(self.simplex)
    
    def set_simplex(self,simplex):
        self.simplex = simplex
        return
    
    def get_person(self):
        return(self.person)
    
    def set_person(self,pers):
        self.person = pers
        return
    
    def get_role(self):
        return(self.role)
    
    def set_role(self,role):
        self.role = role
        return
    