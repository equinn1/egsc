from datetime import datetime, timedelta, date
import copy as cp

class Payperiod():                                #class for dates at end of payperiods
    """Provides a payroll period object given an arbitrary date"""
    def __init__(self,role,check_date):           #constructor
                                                        
        self.school_year     = None               #school year string 'yyyy-yyyy'
        self.school_year_seq = None               #payperiod number within school year 1-26
        self.fiscal_year     = None               #fiscal year  
        self.fiscal_year_seq = None               #payperiod number within fiscal year 1-26
        self.payday          = None               #date checks were issued for this payperiod
        self.checks          = {}                 #dictionary of checks indexed by check number
        self.parent_role     = role               #parent role object
        self.prev_payperiod  = None               #filled in by role when this is added to its payperiod list
        self.next_payperiod  = None               #filled in by role when this is added to its payperiod list
        self.priors          = {}                 #priors for role-dependent paramters
        self.fte_priors      = {}                 #fte priors

        first_payday = self.get_nth_payday_in_fiscal_year(check_date,1) #first payday in fiscal year
        self.fiscal_year = 1 + first_payday.year                      #save fiscal year      
        next_payday = self.get_next_payday(check_date)                #first payday after check date 
        self.payday = next_payday                                     #save payday date
        if (next_payday == first_payday):                             #if first payday in fyear
            self.fiscal_year_seq = 1.0                                #seq = 1
        else:
            tdelta = next_payday - first_payday                       #otherwise compute seq
            self.fiscal_year_seq = 1 + tdelta.days/14                 #as days since first/14 + 1
                                                                      #construct school year string
        syear = str(first_payday.year) + '-' +\
                str(1+first_payday.year)
        first_sy_payday = self.get_nth_payday_in_school_year(syear,1) #get first payday in school year
        if (check_date < first_sy_payday):                     #adjust school year if check is earlier
            self.school_year = str(first_payday.year-1) + '-' + str(first_payday.year)
        else:
            self.school_year = str(first_payday.year) + '-' + str(first_payday.year + 1)
            
        self.school_year_seq = self.fiscal_year_seq - 3         #compute school year sequence number
        if (self.school_year_seq < 1):                   #fiscal year sequence 1,2,3 produce -2,-1,0
            self.school_year_seq += 26                   #convert to 24,25,26

        return
        
    def get_next_payday(self,indate):
        """calculates the next payday on or after an arbitrary input date value"""
        firstdate = date(2009,7,3)
        tdelta = (indate - firstdate)
        ndays = tdelta.days
        newdays = ndays - (ndays % 14)
        if (ndays % 14 == 0):
            npd = firstdate + timedelta(days=newdays)
        else:
            npd = firstdate + timedelta(days=newdays + 14)
        return(npd)
    
    def get_nth_payday_in_fiscal_year(self,indate,n):
        """ Calculates the first payday in the fiscal year of the supplied date"""
        year = indate.year
        month = indate.month
        if (month < 7):
            year=year-1    
        return(self.get_next_payday(date(year,7,1) + timedelta(days=14*(n-1))))

    def get_nth_payday_in_school_year(self,syear,n):
        """ Calculates the nth payday in the given school year supplied as 'yyyy-yyyy' """
        July_1 = date(int(syear[:4]),7,1)               #July 1 of first calenday year 
        return (self.get_nth_payday_in_fiscal_year(July_1,4) + timedelta(days=14*(n-1)))
    
    def get_payday(self):                             #return the last day of the pay period
        """Return payday date"""
        return(self.payday)    
    
    def get_parent_role(self):                        #return the parent role object
        """Return parent role object"""
        return(self.parent_role)    
        
    def get_fiscal_year(self):                        #return the fiscal year
        """Return fiscal year"""
        return(self.fiscal_year)
    
    def get_prev_payperiod(self):
        """Returns previous payperiod object"""
        return(self.prev_payperiod)
    
    def get_next_payperiod(self):
        """Returns next payperiod object"""
        return(self.next_payperiod)
     
    def get_fiscal_year_seq(self):                   #return the fiscal year sequence number
        """Return fiscal year sequence number"""
        return(self.fiscal_year_seq)
    
    def get_school_year_seq(self):                   #return the school year sequence #
        """Return sequence within school year"""
        return(self.school_year_seq)
    
    def get_school_year(self):                        #return the school year
        """Return school year"""
        return(self.school_year)
    
    def add_check(self,check_number,check):
        """Add a check to the check dictionary indexed by check number"""
        self.checks[check_number] = check
        return
    
    def get_check(self,check_number):
        """Retrieve a check from the check dictionary by check number"""
        try:
            return(self.checks[check_number])
        except IndexError:
            return(None)
        except KeyError:
            return(None)
    
    def get_checks(self):
        """Return the check dictionary"""
        return(self.checks)
        
    def get_parent_role(self):
        """Return the parent role object"""
        return(self.parent_role)
    
    def copy_empirical_priors(self,role=None):
        if (role is not None):
            self.priors = cp.deepcopy(self.parent_role.empirical_priors)
        else:
            self.priors = cp.deepcopy(self.parent_role.empirical_priors[role])
        return
    
    def get_priors(self):
        return(cp.deepcopy(self.priors))
    
    def get_fte_priors(self,ftekey=None):
        if (ftekey is None):
            return(cp.deepcopy(self.fte_priors))
        else:
            try:
                return(cp.deepcopy(self.fte_priors[ftekey]))
            except KeyError:
                print('KeyError in get_fte_priors: ',ftekey)
                return
    
    def set_priors(self,priors):
        self.priors = cp.deepcopy(priors)
        return
    
    def set_fte_priors(self,priors):
        self.fte_priors = cp.deepcopy(priors)
        return
    
    def set_fte_priors_by_key(self,ftekey,priors):
        self.fte_priors[ftekey] = cp.deepcopy(priors)
        return
    
    def set_prev_payperiod(self,pperiod):
        self.prev_payperiod = pperiod
        return
    
    def set_next_payperiod(self,pperiod):
        self.next_payperiod = pperiod
        return

    def copy_priors_forward(self):
        next_pp = self.next_payperiod
        if (self.get_next_payperiod() is not None):
            next_pp.set_priors(cp.deepcopy(self.get_priors()))
            next_pp.set_fte_priors(cp.deepcopy(self.get_fte_priors()))
        return

    def get_previous_payperiod(self):
        return(self.prev_payperiod)
    
    def likelihood_order(self,dct):
        """Returns the index array for sorting a vector of probabilities in descending order"""
        vals = {}
        for key in dct.keys():
            val = dct[key]
            if val not in vals.keys():
                vals[val] = []
            vals[val].append(key)

        ixa = []
        for kval in sorted(vals.keys(),reverse=True):
            for ix in vals[kval]:
                ixa.append(ix)
                
        return(ixa)