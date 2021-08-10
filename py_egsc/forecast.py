from datetime import datetime, timedelta, date
from pay_check import Pay_check, Check_lineitem
import copy as cp
import numpy as np
from numpy.random import choice
from roles_Bayes import * 

class Forecast():         #class for forecast
    """Provides a forecast object"""
    def __init__(self,school_year,n_years,base,desc1,desc2,changes={}):      #constructor
        self.base_school_year     = base[0]           #base year string 'yyyy-yyyy'
        self.base_school_year_seq = base[1]           #payperiod in base year
        self.school_year          = school_year       #first forecast school year string 'yyyy-yyyy'
        self.forecast_years       = n_years           #number of years to forecast
        self.desc1                = desc1             #first description line
        self.desc2                = desc2             #second description line
        self.changes              = changes           #dictionary of percent changes for salaries by role
        self.forecast_years       = self.list_forecast_years()      #forecast school years
        self.factors              = self.compute_factors(self.changes)  #increase factors
        self.run_date             = date.today()                                            #run date
        self.forecast_summary     = {}                #[school_year][role_class][role_name][payment_type]
        self.forecast_detail      = {}                #[school_year][role_class][role_name][name][syseq]
        self.actual_summary       = {}                #[school_year][payment_type][role_class]
        self.actual_detail        = {}                #[school_year][payment_type][role_class][role_name][name]
         
        return
 
    def get_school_year(self):
        return(self.school_year)
    
    def get_base_school_year(self):
        return(self.base_school_year)
    
    def set_base_school_year(self,byear):
        self.base_school_year = byear
        return
    
    def get_base_school_year_seq(self):
        return(self.base_school_year_seq)
    
    def set_base_school_year_seq(self,syseq):
        self.base_school_year_seq = syseq
        return
    
    def set_school_year(self,syear):
        self.school_year = syear
        return
    
    def get_changes(self):
        return(self.changes)
  
    def get_desc(self):
        return((self.desc1,self.desc2))
    
    def set_desc(self,desc1,desc2):
        self.desc1 = desc1
        self.desc2 = desc2
        return
 
    def set_changes(self,changes):
        self.changes = changes
        return
  
    def list_forecast_years(self):
        fc_years = []
        Fall_year = int(self.school_year[0:4])
        for i in np.arange(0,self.forecast_years):
            Spring_year = Fall_year + 1
            systring = str(Fall_year)+'-'+str(Spring_year)
            fc_years.append(systring)
            Fall_year = Spring_year
        return(fc_years)
    
    def get_next_school_year(self,school_year):
        y = school_year[5:]
        return(y + '-' + str(int(y)+1))
    
    def get_previous_school_year(self,school_year):
        y = int(school_year[0:4])
        return(str(y-1) + '-' + str(y))
    
    def compute_factors(self,changes):
        factors = {}
        for key in changes.keys():
            sy = changes['Start year']
            if ('Start' not in key):
                factors[key] = {}
                multiplier = 1.0
                pcts = changes[key]
                for i in np.arange(len(pcts)):
                    multiplier = round(multiplier*(1.0 + pcts[i]/100.0),4)
                    factors[key][sy] = multiplier
                    sy = self.get_next_school_year(sy)
        return(factors)
    
    def get_factors(self):
        return(self.factors)
    
    def get_forecast_years(self):
        return(self.forecast_years)
    
    def set_forecast_years(self,fylist):
        self.forecast_years = fylist
        return
    
    def get_run_date(self):
        return(self.run_date)
    
    def get_forecast_detail(self):
        return(self.forecast_detail)
    
    def get_forecast_summary(self):
        return(self.forecast_summary)
    
    def get_actual_detail(self):
        return(self.actual_detail)
    
    def get_actual_summary(self):
        return(self.actual_summary)
    
    def build_forecast(self,people):           #input is decoded payroll
        """Build forecast from decoded payroll data"""
        for name in people.keys():                                               #loop through people
            roles = people[name].get_roles()                                     #loop through roles
            for role_name in roles.keys():                                       #get role names
                role = roles[role_name]                                     
                role_class = role.get_role_class()                               #get role class
                pp = role.get_payperiods()                                       #get payperiods
                for syear in pp.keys():                                          #loop through school hears
                    if (syear == self.base_school_year):                         #take years 
                        for syseq in pp[syear].keys():                           #if so get payperiods
                            if (syseq <= self.base_school_year_seq):
                                chks = pp[syear][syseq].get_checks()             #get checks for this payperiod
                                for chk in chks:                                 #loop through checks
                                    lis = chks[chk].get_items()                  #get line items for each check
                                    for i in lis.keys():                         #loop through line items
                                        itm = lis[i]
                                        payment = Actual_payment(self,itm)       #create actual_payment object
                                        self.add_payment(self.actual_detail,payment) #add it to the list     
                                        role.compute_forecast(self,payment)      #call compute forecast routine for role
                role.complete_forecast(self,role_class,role_name,name,people)    #fill in remaining periods
        return
    
    def add_payment(self,dd,pmt,incr = 0):  #[school_year][role_class][role_class][payment_type][role_name][name][syseq]
        """Add a pyment to the appropriate dictionary"""
        syear = pmt.get_school_year()                                             #get school year for payment
        syseq = incr + pmt.get_school_year_seq()                                         #get sy sequence for payment (1-26)
        role_name = pmt.get_role_name()                                           #get role name
        role_class = pmt.get_role_class()                                         #get role class
        payment_type = pmt.get_payment_type()                                     #get payment type
        name = pmt.get_name()                                                     #get person's name
        if syear not in dd.keys():                                                #make sure school year has an entry
            dd[syear] = {}
        if role_class not in dd[syear].keys():                                    #make sure role class has an entry
            dd[syear][role_class] = {}
        if role_name not in dd[syear][role_class].keys():                         #make sure role name has an entry
            dd[syear][role_class][role_name] = {}
        if payment_type not in dd[syear][role_class][role_name].keys():           #make sure payment type has an entry
            dd[syear][role_class][role_name][payment_type] = {}
        if name not in dd[syear][role_class][role_name][payment_type].keys():     #make sure person's name has an entry
            dd[syear][role_class][role_name][payment_type][name] = {}
        if syseq not in dd[syear][role_class][role_name][payment_type][name].keys():
            dd[syear][role_class][role_name][payment_type][name][syseq] = []      #make sure payperiod has an entry
        dd[syear][role_class][role_name][payment_type][name][syseq].append(pmt)   #append this payment to the list
        return
        
class Payment():
    """Parent class for payment"""
    
    def __init__(self):
        self.payment_types = {1:'Contract salary',
                              2:'One-time stipend',
                              3:'Class coverage', 
                              4:'Contract rate',
                              5:'Detention coverage',
                              6:'Contract salary adjustment',
                              7:'Contract rate: step 7 stipend',
                              8:'Class coverage', 
                              9:'Other additional compensation', 
                              10:'Contract overtime rate',
                              11:'Health and Medical',
                              12:'Early Retirement Incentive',
                              13:'Mentoring',
                              14:'Stipend - Coaches/Advisors',
                              15:'Stipend - other', 
                              16:'Professional Development and Training Services',
                              17:'Class Overage/Weighting',
                              18:'Stipend - mentors',
                              19:'Coverage - other',
                              20:'Professional Development and Training',
                              21:'Summer Pay',
                              22:'Stipend - Athletic Officials',
                              23:'Officials/Referees',
                              24:'nosuch',
                              25:'Coach/Advisor stipend',
                              26:'Added stipend', 
                              27:'Head custodian stipend',
                              28:'Head custodian stipend - Middle School',
                              30:'Maintenance Foreman stipend',
                              31:'Head custodian stipend - OT',
                              32:'Head custodian stipend - Middle School - OT',
                              35:'Overtime',
                              36:'Facilities stipend',
                              38:'Obj 20430',
                              39:'Custodian part time',
                              40:'Mysterious 1/5/2018',
                              99:'Other or unknown'}
        
        def get_payment_types(self):
            """Get list of payment types"""
            return(self.payment_types)
        
        def check_payment_types(self,pt):
            """Check if a payment type is in the list"""
            found = False
            for i in self.payment_types.keys():
                if (self.payment_types[i] == pt):
                    found = True
            return(found)

class Forecast_payment(Payment):              #class for forecast payment
    """Subclass for forecast payment"""
    def __init__(self,fc,pmt,syear,syseq,earnings,stepinfo):
        Payment.__init__(self)
        self.parent_forecast = fc   
        self.payment_type    = pmt.get_payment_type()       #keep same payment type
        self.role            = pmt.get_role()               #same parent role
        self.role_class      = pmt.get_role_class()         #same parent role class
        self.role_name       = pmt.get_role_name()          #same parent role name
        self.person          = pmt.get_person()             #same parent person
        self.name            = self.person.get_name()       #same name
        self.earnings        = earnings                     #earnings from forecast routine
        self.acct            = pmt.get_acct()               #same acct
        self.obj             = pmt.get_obj()                #same obj
        self.stepinfo        = stepinfo                     #stepinfo from forecast routine
        self.school_year     = syear                        #school_year from forecast routine
        self.school_year_seq = syseq                        #school_year_sequence from forecast routine
        self.fiscal_year     = None                         #maybe later
        self.fiscal_year_seq = None                         #maybe later
        self.base_payment    = pmt                          #base period payment
        return
    
    def get_person(self):
        return(self.person)
    
    def set_person(self,pers):
        self.person = pers
        return
    
    def get_role(self):
        return(self.role)
    
    def set_role(self,role_name):
        self.role = role_name
        return
    
    def get_payment_type(self):
        return(self.payment_type)
    
    def set_payment_type(self,pt):
        self.payment_type = pt
        return
    
    def get_base_payment(self):
        return(self.payment)
    
    def set_base_payment(self,pmt):
        self.payment = pmt
        return
    
    def get_earnings(self):
        return(self.earnings)
    
    def set_earnings(self,earnings):
        self.earnings = earnings
        return
    
    def get_stepinfo(self):
        return(self.stepinfo)
    
    def set_stepinfo(self,stepinfo):
        self.stepinfo = stepinfo
        return
    
    def get_role_name(self):                                 
        return(self.role_name)
    
    def set_role_name(self,role_name):
        self.role_name = role_name
        returnv
    
    def get_role_class(self):                             
        return(self.role_class)
    
    def get_acct(self):
        return(self.acct)
    
    def set_acct(self,acct):
        self.acct = acct
        return
    
    def get_obj(self):
        return(self.obj)
    
    def set_obj(self,obj):
        self.obj = obj
        return
    
    def get_payment_types(self):
        return(self.payment_types)
    
    def get_fiscal_year(self):                        #return the fiscal year
        """Return fiscal year"""
        return(self.fiscal_year)
    
    def set_fiscal_year(self,fiscal_year):
        self.fiscal_year = fiscal_year
        return
     
    def get_fiscal_year_seq(self):                   #return the fiscal year sequence number
        """Return fiscal year sequence number"""
        return(self.fiscal_year_seq)
    
    def set_fiscal_year_seq(self,fiscal_year_seq):
        self.fiscal_year_seq = fiscal_year_seq
        return
    
    def get_school_year_seq(self):                   #return the school year sequence #
        """Return sequence within school year"""
        return(self.school_year_seq)
    
    def set_school_year_seq(self,school_year_seq):
        self.school_year_seq = school_year_seq
        return
    
    def get_school_year(self):                        #return the school year
        """Return school year"""
        return(self.school_year)
    
    def set_school_year(self,school_year):
        self.school_year = school_year
        return
    
    def get_name(self):
        return(self.name)
    
    def set_name(self,name):
        self.name = name
        return
    
class Actual_payment(Payment):              #class for payment type categories
    """Subclass for actual payment"""
    def __init__(self,fc,linitem):                   #constructor
        Payment.__init__(self)
        self.parent_forecast = fc                                                
        self.line_item       = linitem            #parent lineitem
        self.line_item_number = None
        self.cumulative      = False              #cumulative payment?
        self.start_date      = None               #start paydate for cumulative
        self.end_date        = None               #end paydate for cumulative
        self.payment_type    = self.line_item.get_payment_type()              #payment type
        self.check           = self.line_item.get_parent_check()  #parent check
        self.ckdate          = self.check.get_date()
        self.payperiod       = self.check.get_parent_payperiod()  #parent payperiod
        self.role            = self.payperiod.get_parent_role()   #parent role
        self.role_class      = self.role.get_role_class()         #parent role class
        self.role_name       = self.role.get_role_name()          #parent role name
        self.person          = self.role.get_parent_person()      #parent person
        self.name            = self.person.get_name()             #name
        self.rate            = self.line_item.get_rate()          #rate
        self.earnings        = self.line_item.get_earnings()      #earnings from parent lineitem
        self.acct            = self.line_item.get_acct()          #acct code from parent lineitem
        self.obj             = self.line_item.get_obj()           #obj code from parent lineitem
        self.stepinfo        = self.line_item.get_stepinfo()      #stepinfo from parent lineitem
        self.check_number    = self.check.get_number()            #check number
        self.school_year     = self.payperiod.get_school_year()   #school year from payperiod
        self.school_year_seq = self.payperiod.get_school_year_seq()
        self.fiscal_year     = self.payperiod.get_fiscal_year()   #fiscal year from payperiod
        self.fiscal_year_seq = self.payperiod.get_fiscal_year_seq()
    
    def get_person(self):
        return(self.person)
    
    def get_role(self):
        return(self.role)
    
    def get_payperiod(self):
        return(self.payperiod)
    
    def get_payment_type(self):
        return(self.payment_type)
    
    def get_check(self):
        return(self.check)
    
    def get_check_number(self):
        return(self.check_number)
    
    def get_check_date(self):
        return(self.ckdate)
    
    def get_lineitem(self):
        return(self.line_item)
    
    def get_cumulative(self):
        return(self.cumulative)
    
    def set_cumulative(self,lval):
        self.cumulative = lval
        return
    
    def get_earnings(self):
        return(self.earnings)
    
    def get_stepinfo(self):
        return(self.stepinfo)
    
    def get_role_name(self):                                 
        return(self.role_name)
    
    def get_role_class(self):                             
        return(self.role_class)
    
    def get_acct(self):
        return(self.acct)
    
    def get_obj(self):
        return(self.obj)
    
    def get_payment_types(self):
        return(self.payment_types)
    
    def get_fiscal_year(self):                        #return the fiscal year
        """Return fiscal year"""
        return(self.fiscal_year)
     
    def get_fiscal_year_seq(self):                   #return the fiscal year sequence number
        """Return fiscal year sequence number"""
        return(self.fiscal_year_seq)
    
    def get_school_year_seq(self):                   #return the school year sequence #
        """Return sequence within school year"""
        return(self.school_year_seq)
    
    def get_school_year(self):                        #return the school year
        """Return school year"""
        return(self.school_year)
    
    def get_name(self):
        return(self.name)
 