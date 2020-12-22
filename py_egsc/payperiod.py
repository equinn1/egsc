from datetime import datetime, timedelta, date

class Payperiod():                                      #class for dates at end of payperiods
    """Provides a payroll period object"""
    def __init__(self,arg1,seq=None):                   #constructor
        
        self.school_year_seq = None
        self.checks = {}
        self.scenarios = {}

        if seq is not None:                             #called with fiscal year and sequence number
            self.fyear = arg1                           #fiscal year is first argument
            self.seq   = seq                            #sequence number is second argument
            self.set_payday()                           #set date of payday
            self.set_school_year()
            
        else:                                           #called with just a date
            self.set_fiscal_year_and_payday(arg1)       #set fiscal year and payday       
        
        self.calendar_year = self.payday.year           #set calendar year

        return

    def set_fiscal_year_and_payday(self,arg1):
        check_date = arg1                               #first argument is check date
        delta = timedelta(days=14)                      #14 days per pay period
        pdate = date(2009,7,3)                          #first payperiod end
        lmonth = 6                                      #previous month
        seq = 1                                         #fiscal year sequence number
        while(pdate < check_date):                      #loop through at 14 day increments
            pmonth = pdate.month                        #payday month
            if ((lmonth == 6) & (pmonth == 7)):         #only if prev check in June, current in July
                seq = 1                                 #fiscal year payperiod number is one
                fyear = pdate.year + 1                  #fiscal year is pdate year plus 1
            else:                                       #otherwise:
                seq += 1                                #increment fiscal year payperiod seq
            self.seq = seq                              #set payday number
            lmonth = pmonth                             #finally set last month to payday month
            pdate += delta                              #until we find payday >= given date
            self.payday = pdate                         #payday is first pay date >= cdate
        self.seq += 1
        if (self.seq > 26):
            self.seq = 1
        if (self.seq < 4):
            self.school_year_seq = self.seq + 23
        else:
            self.school_year_seq = self.seq - 3
        if ((self.payday.month < 8) | ((self.payday.month==8) & (self.school_year_seq > 23))):
            self.school_year = str(self.payday.year-1) + '-' + str(self.payday.year)
        else:
            self.school_year = str(self.payday.year) + '-' + str(self.payday.year+1)
        if (self.payday.month < 7):
            self.fyear = self.payday.year
        else:
            self.fyear = self.payday.year + 1
        
         
        return
    
    
    def set_school_year_seq(self):
        self.school_year_seq = self.seq - 3
        if self.school_year_seq < 1:
            self.school_year_seq = 26 + self.school_year_seq
        return
    
    def set_payday(self):
        payday = date(2009,7,3)                         #first pay period of FY2010
        lmonth = 6
        delta = timedelta(days=14)                      #14 days per pay period
        fy = 2009                                       #initial fiscal year is 2009
        seq = 1
        lmonth = 6
        while(fy < self.fyear):
            cmonth = payday.month
            payday += delta                        #in 14 day increments
            if ((lmonth==6) & (cmonth==7)):
                fy = 1 + payday.year
                seq = 1
            else:
                seq += 1
            lmonth = cmonth
        self.payday = payday + (self.seq-1)*delta
        return
        
    def set_school_year(self):                                            #determine school year
        self.school_year = str(self.fyear - 1) + '-' + str(self.fyear)    # fyear to fyear + 1
        if self.seq < 4:                                                  #except first three paydays
            self.school_year = str(self.fyear - 2) + '-' + str(self.fyear-1)  # then fyear-1 to fyear
        return
    
    def get_payday(self):                             #return the last day of the pay period
        """Lookup end date of payroll periods in a given fiscal year"""
        return(self.payday)    
        
    def get_fiscal_year(self):                        #return the fiscal year
        """Return fiscal year"""
        return(self.fyear)
     
    def get_payperiod_number(self):                   #return the fiscal year
        """Return fiscal year"""
        return(self.seq)
    
    def get_school_year_seq(self):                   #return the fiscal year
        """Return sequence within school year"""
        return(self.school_year_seq)
    
    def get_school_year(self):                        #return the school year
        """Return school year"""
        return(self.school_year)
    
    def get_previous_payday(self):                    #find date of the previous payday
        """Find the date of the previous payday"""
        return(self.payday - timedelta(days=14))
    
    def get_next_payday(self):                       #find date of the next payday
        """Find the date of the next payday"""
        return(self.payday + timedelta(days=14))
    
    def add_check(self,check_number,check):
        self.checks[check_number] = check
        return
    
    def add_scenario(self,scenario_id,scenario):
        self.scenarios[scenario_id] = scenario
        return
    
    def get_checks(self):
        return(self.checks)
    
    def get_calendar_year(self):
        return(self.calendar_year)