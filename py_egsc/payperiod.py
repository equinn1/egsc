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
            
        else:                                           #called with just a date
            self.set_fiscal_year_and_payday(arg1)       #set fiscal year and payday       
            self.set_school_year()
            
        self.set_school_year()                          #set school year
        self.school_year_seq = None
        self.set_school_year_seq()                      #set school year sequence number
        self.calendar_year = self.payday.year           #set calendar year

        return

    def set_fiscal_year_and_payday(self,cdate):
        delta = timedelta(days=14)                      #14 days per pay period
        pdate = date(2009,7,3)                          #first payperiod end
        seq = 0                                         #payperiod sequence number for this date
        while(pdate < cdate):                           #loop through at 14 day increments
            pdate += delta                              #until we find payday >= given date
            seq += 1                                    #keep incrementing sequence number
        self.payday = pdate                             #payday is first pay date >= cdate
        self.fyear = self.payday.year - 1               #set fiscal year according to month
        if (self.payday.month > 6):
            self.fyear += 1
        self.seq = 1 + ((seq - 1) % 26)                 #recover sequence number for this fyear
        return
    
    def set_school_year_seq(self):
        self.school_year_seq = self.seq - 3
        if self.school_year_seq < 1:
            self.school_year_seq = 26 - self.school_year_seq
        return
    
    def set_payday(self):
        self.payday = date(2009,7,3)                    #first pay period of FY2010
        delta = timedelta(days=14)                      #14 days per pay period
        fy = 2010                                       #initial fiscal year is 2010
        while(fy < self.fyear):                         #loop until fiscal year is >= supplied fyear
            self.payday += delta                        #in 14 day increments
            fy = self.payday.year                       #recompute fiscal year for new payday
            if self.payday.month < 7:
                fy= fy - 1
        self.payday += timedelta(days=int(14*(self.seq-1)))  #add 14 days for each payday past first
        return
        
    def set_school_year(self):                                            #determine school year
        self.school_year = str(self.fyear) + '-' + str(self.fyear + 1)    # fyear to fyear + 1
        if self.seq < 4:                                                  #except first three paydays
            self.school_year = str(self.fyear - 1) + '-' + str(self.fyear)  # then fyear-1 to fyear
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