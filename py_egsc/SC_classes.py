from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class payperiod():                                      #class for dates at end of payperiods
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
    
class EG_acct_codes():
    def __init__(self):
        self.EG_account_codes ={
            '71100105': 'K Frenchtown',
            '71100107': 'K MDBK',
            '71109105': 'Title 1  Frenchtown',
            '71109107': 'Title 1  MDBK',
            '71110105': 'Grade 1 Frenchtown',
            '71110107': 'Grade 1 MDBK',
            '71120105': 'Grade 2 Frenchtown',
            '71120107': 'Grade 2 MDBK',
            '71121102': 'Art Eldredge',
            '71121103': 'Art Cole',
            '71121105': 'Art Frenchtown',
            '71121106': 'Art EGHS',
            '71121107': 'Art MDBK',
            '71121108': 'Art Hanaford',
            '71123103': 'ELA Cole',
            '71123106': 'ELA EGHS',
            '71123108': 'ELA Hanaford',
            '71124103': 'Foreign Language Cole',
            '71124106': 'Foreign Language EGHS',
            '71125102': 'PE/health Eldredge',
            '71125103': 'PE/health Cole',
            '71125105': 'PE/health Frenchtown',
            '71125106': 'PE/health EGHS',
            '71125107': 'PE/health MDBK',
            '71125108': 'PE/health Hanaford',
            '71126103': 'Tech Cole',
            '71126306': 'Tech EGHS',
            '71127103': 'Math Cole',
            '71127106': 'Math EGHS',
            '71128102': 'Music Eldredge',
            '71128103': 'Music Cole',
            '71128105': 'Music Frenchtown',
            '71128106': 'Music EGHS',
            '71128107': 'Music MDBK',
            '71128108': 'Music Hanaford',
            '71129103': 'Science Cole',
            '71129106': 'Science EGHS',
            '71130102': 'Grade 3 Eldredge',
            '71130105': 'Grade 3 Frenchtown',
            '71130108': 'Grade 3 Hanaford',
            '71130406': 'Business/Computer  EGHS',
            '71131103': 'Social Studies Cole',
            '71131106': 'Social Studies EGHS',
            '71140102': 'Grade 4 Eldredge',
            '71140108': 'Grade 4 Hanaford',
            '71140403': 'Computer Cole',
            '71140406': 'Computer EGHS',
            '71141102': 'Reading Eldredge',
            '71141103': 'Reading Cole',
            '71141105': 'Reading Frenchtown',
            '71141106': 'Reading EGHS',
            '71141107': 'Reading MDBK',
            '71141108': 'Reading Hanaford',
            '71150102': 'Grade 5 Eldredge',
            '71150108': 'Grade 5 Hanaford',
            '71180102': 'SPED Eldredge',
            '71180103': 'SPED EGHS',
            '71180105': 'SPED Frenchtown',
            '71180106': 'SPED EGHS',
            '71180107': 'SPED MDBK',
            '71180108': 'SPED Hanaford',
            '71181102': 'SPED Life Skills Eldredge',
            '71181103': 'SPED Life Skills Cole',
            '71181105': 'SPED Life Skills Frenchtown',
            '71181106': 'SPED Life Skills EGHS',
            '71181107': 'SPED Life Skills MDBK',
            '71182107': 'SPED EGHS',
            '71191302': 'ESL Eldredge',
            '71191303': 'ESL Cole',
            '71191305': 'ESL Frenchtown',
            '71191306': 'ESL EGHS',
            '71191307': 'ESL MDBK',
            '71191308': 'ESL Hanaford',
            '71210202': 'Teacher Subs Eldredge',
            '71210203': 'Teacher Subs Cole',
            '71210205': 'Teacher Subs Frenchtown',
            '71210206': 'Teacher Subs EGHS',
            '71210207': 'Teacher Subs MDBK',
            '71210208': 'Teacher Subs Hanaford',
            '71210402': 'Long Term Subs Eldredge',
            '71210403': 'Long Term Subs Cole',
            '71210405': 'Long Term Subs Frenchtown',
            '71210406': 'Long Term Subs EGHS',
            '71210407': 'Long Term Subs MDBK',
            '71210408': 'Long Term Subs Hanaford',
            '71223102': 'Para Subs Eldredge',
            '71223103': 'Para Subs Cole',
            '71223105': 'Para Subs Frenchtown',
            '71223106': 'Para Subs EGHS',
            '71223107': 'Para Subs MDBK',
            '71223108': 'Para Subs Hanaford',
            '71231503': 'Guidance Cole',
            '71231506': 'Guidance EGHS',
            '71246702': 'Librarian Eldredge',
            '71246703': 'Librarian Cole',
            '71246705': 'Librarian Frenchtown',
            '71246706': 'Librarian EGHS',
            '71246707': 'Librarian MDBK',
            '71246708': 'Librarian Hanaford',
            '71269102': 'Other Compensation-Eldredge',
            '71269103': 'Other Compensation-Cole',
            '71269105': 'Other Compensation-Frenchtown',
            '71269106': 'Other Compensation-EGHS',
            '71269107': 'Other Compensation-MDBK',
            '71269108': 'Other Compensation-Hanaford',
            '71269506': 'Nurse EGHS',
            '71270102': 'Nurse Subs Eldredge',
            '71270103': 'Nurse Subs Cole',
            '71270105': 'Nurse Subs Frenchtown',
            '71270106': 'Nurse Subs EGHS',
            '71270107': 'Nurse Subs MDBK',
            '71270108': 'Nurse Subs Hanaford',
            '71270302': 'Nurse Eldredge',
            '71270303': 'Nurse Cole',
            '71270305': 'Nurse Frenchtown',
            '71270306': 'Nurse EGHS',
            '71270307': 'Nurse MDBK',
            '71270308': 'Nurse Hanaford',
            '71272606': 'Dept Head-Guidance',
            '71278106': 'Dept Head-SPED',
            '71278406': 'Dept Head-ELA',
            '71278506': 'Dept Head-FLA',
            '71279206': 'Dept Head-HPE',
            '71279306': 'Dept Head-Math',
            '71279406': 'Dept Head-NSci',
            '71279506': 'Dept Head-SocS',
            '71295120': 'Dept Head-SOCW',
            '71301106': 'SPED EGHS',
            '71301602': 'Social Worker Eldredge',
            '71301603': 'Social Worker Cole',
            '71301605': 'Social Worker Frenchtown',
            '71301606': 'Social Worker EGHS',
            '71301607': 'Social Worker MDBK',
            '71301608': 'Social Worker Hanaford',
            '71302702': 'OT Eldredge',
            '71302703': 'OT Cole',
            '71302705': 'OT Frenchtown',
            '71302706': 'OT EGHS',
            '71302707': 'OT MDBK',
            '71302708': 'OT Hanaford',
            '71308102': 'Adaptive PE Eldredge',
            '71308103': 'Adaptive PE Cole',
            '71308105': 'Adaptive PE Frenchtown',
            '71308106': 'Adaptive PE EGHS',
            '71308107': 'Adaptive PE MDBK',
            '71308108': 'Adaptive PE Hanaford',
            '71310106': 'History EGHS',
            '71311702': 'Psychologist Eldredge',
            '71311703': 'Psychologist Cole',
            '71311705': 'Psychologist Frenchtown',
            '71311706': 'Psychologist EGHS',
            '71311707': 'Psycholotist MDBK',
            '71311708': 'Psychologist Hanaford',
            '71321802': 'Speech Eldredge',
            '71321803': 'Speech Cole',
            '71321805': 'Speech Frenchtown',
            '71321806': 'Speech EGHS',
            '71321807': 'Speech MDBK',
            '71321808': 'Speech Hanaford',
            '71347302': 'Custodian Subs Eldredge',
            '71347303': 'Custodian Subs Cole',
            '71347305': 'Custodian Subs Frenchtown',
            '71347306': 'Custodian Subs EGHS',
            '71347307': 'Custodian Subs MDBK',
            '71347308': 'Custodian Subs Hanaford'
        }
        self.EG_account_codes6 ={
            '711001': 'K',
            '711091': 'Title 1',
            '711101': 'Grade 1',
            '711201': 'Grade 2',
            '711211': 'Art',
            '711231': 'ELA',
            '711241': 'Foreign Language',
            '711251': 'PE/health',
            '711261': 'Tech',
            '711271': 'Math',
            '711281': 'Music',
            '711291': 'Science',
            '711301': 'Grade 3',
            '711304': 'Business/Computer',
            '711311': 'Social Studies',
            '711401': 'Grade 4',
            '711404': 'Computer',
            '711411': 'Reading',
            '711501': 'Grade 5',
            '711801': 'SPED',
            '711811': 'SPED Life',
            '711821': 'SPED EGHS',
            '711913': 'ESL',
            '712102': 'Teacher Subs',
            '712104': 'Long Term Subs',
            '712231': 'Para Subs',
            '712315': 'Guidance',
            '712467': 'Librarian',
            '712691': 'Additional Coverage',
            '712693': 'Additional Coverage',
            '712695': 'Nurse EGHS',
            '712701': 'Nurse Subs',
            '712703': 'Nurse',
            '712726': 'Dept Head-Guidance',
            '712781': 'Dept Head-SPED',
            '712784': 'Dept Head-ELA',
            '712785': 'Dept Head-FLA',
            '712792': 'Dept Head-HPE',
            '712793': 'Dept Head-Math',
            '712794': 'Dept Head-NSci',
            '712795': 'Dept Head-SocS',
            '712697': 'Additional Coverage',
            '713011': 'SPED EGHS',
            '713016': 'Social Worker',
            '713027': 'OT',
            '713081': 'Adaptive PE',
            '713101': 'History',
            '713117': 'Psychologist',
            '713218': 'Speech',
            '713473': 'Custodian Subs'
        }
        self.local6_to_ucoa = {
            '71295120': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 1,'JC':1100}
        }
        self.local_to_ucoa = {
            '711001': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1,'JC':1100},
            '711101': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 3,'JC':1100},
            '711201': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 4,'JC':1100},
            '711301': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 5,'JC':1100},
            '711401': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 6,'JC':1100},
            '711501': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 7,'JC':1100},
            '711211': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 200,'JC':1100},
            '711231': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 500,'JC':1100},
            '711241': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 700,'JC':1100},
            '711251': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1200,'JC':1100},
            '711271': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1500,'JC':1100},
            '711281': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1600,'JC':1100},
            '711291': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1700,'JC':1100},
            '711311': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1900,'JC':1100},
            '711411': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 2400,'JC':1100},
            '711261': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 2000,'JC':1100},
            '711404': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 2000,'JC':1100},
            '712467': {'Fund':1000000,'Prog':10,'Func':212,'Sub': 2600,'JC':1600},
            '712726': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 800,'JC':1500},
            '712781': {'Fund':1000000,'Prog':20,'Func':221,'Sub': 2101,'JC':1100},
            '712784': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 500,'JC':1100},
            '712785': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 700,'JC':1100},
            '712792': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 1200,'JC':1100},
            '712793': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 1500,'JC':1100},
            '712794': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 1700,'JC':1100},
            '712795': {'Fund':1000000,'Prog':10,'Func':221,'Sub': 1900,'JC':1100},
            '713027': {'Fund':1000000,'Prog':20,'Func':232,'Sub': 2125,'JC':1700},
            '713218': {'Fund':1000000,'Prog':20,'Func':232,'Sub': 2122,'JC':1700},
            '713117': {'Fund':1000000,'Prog':20,'Func':232,'Sub': 2121,'JC':1700},
            '713016': {'Fund':1000000,'Prog':20,'Func':232,'Sub': 2120,'JC':1700},
            '719130': {'Fund':1000000,'Prog':40,'Func':111,'Sub': 600,'JC':1300},
            '711304': {'Fund':1000000,'Prog':10,'Func':111,'Sub': 1800,'JC':1100},
            '712315': {'Fund':1000000,'Prog':10,'Func':211,'Sub': 800,'JC':1500}
        }
        return
    
    def get_loc_from_acct(self,acct,ucl):
        uc = {}
        locd={'02':'3102','08':'3108','07':'3107','06':'5106','03':'4103','05':'3105'}
        loc2 = acct[6:]
        try:
            uc['Loc'] = locd[loc2]
            uc['Location Description'] = ucl.get_label('Loc',uc['Loc'])
            return(uc)
        except KeyError:
            return(uc)
        return
    
    def get_UCOA_from_acct(self,acct,ucl):
        ucd = {}
        locd={'02':'3102','08':'3108','07':'3107','06':'5106','03':'4103','05':'3105'}
        acct6 = acct[:6]
        try:
            uc = self.local_to_ucoa[acct6]
            uc['acct'] = acct
            uc['Program Description'] = ucl.get_label('Prog',uc['Prog'])
            uc['Function Description'] = ucl.get_label('Func',uc['Func'])
            uc['Subject Description'] = ucl.get_label('Sub',uc['Sub'])
            uc['Job Class Description'] = ucl.get_label('JC',uc['JC'])
            loc2 = acct[6:]
            try:
                uc['Loc'] = locd[loc2]
                uc['Location Description'] = ucl.get_label('Loc',uc['Loc'])
                return(uc)
            except KeyError:
                return(uc)
        except KeyError:
            uc = {}
            return(uc)
        return
    
    def get_UCOA_from_acct6(self,acct6,ucl):
        ucd = {}
        try:
            uc = self.local_to_ucoa[acct6]
            uc['acct6'] = acct6
            uc['Program Description'] = ucl.get_label('Prog',uc['Prog'])
            uc['Function Description'] = ucl.get_label('Func',uc['Func'])
            uc['Subject Description'] = ucl.get_label('Sub',uc['Sub'])
            uc['Job Class Description'] = ucl.get_label('JC',uc['JC'])
        except KeyError:
            uc = {}
            return(uc)
        return(uc)
            
        
    def get_eg_acct_desc(self,acct):
        """Provides descriptions for accounting codes in EG MUNIS system."""
        try:
            return(self.EG_account_codes[acct])
        except KeyError:
            return('(no description)')
        
    def get_eg_acct_desc6(self,acct):
        """Provides descriptions for accounting codes in EG MUNIS system."""
        try:
            return(self.EG_account_codes6[acct])
        except KeyError:
            return('(no description)')
        
    def check_eg_acct_desc6(self,acct):
        """ check whether first 6 digits map an acct6 key"""
        return(acct in self.EG_account_codes6.keys())
        
    def get_eg_acct_UCOA(self,acct):
        """Provides UCOA codes for accounting codes in EG MUNIS system."""
        try:
            return(self.local_to_ucoa[acct])
        except KeyError:
            return({})
        
    def get_eg_acct_codes(self):
        """Returns dictionary of account codes."""
        return(self.EG_account_codes)
    
class pay_check():                                                            #generic check class
    def __init__(self,check_number,name,check_date):                          #constructor
        self.check_number   = check_number
        self.name           = name
        self.check_date     = check_date
        self.items          = {}
        return

    def get_name(self):
        return(self.name)
    
    def get_school_year(self):
        yy = self.check_date.year
        boundry = date(yy,8,14)
        if (self.check_date <= boundry):
            syear = str(yy-1) + '-' + str(yy)
        else:
            syear = str(yy) + '-' + str(yy + 1)
        return(syear)
        
    def get_date(self):
        return(self.check_date)
    
    def get_number(self):
        return(self.check_number)
   
    def get_items(self):
        return(self.items)
    
    def add_item(self,check_lineitem):
        item_number = len(self.items) + 1
        self.items[item_number] = check_lineitem
        return
    
class check_lineitem():                                                       #check lineitem class
    def __init__(self,fund,acct,obj,position,rate,earnings,acct_desc,obj_desc,acct_UCOA,stepinfo):
        self.fund = fund
        self.acct = acct
        self.obj  = obj
        self.position = position
        self.rate = rate
        self.earnings = earnings
        self.acct_desc = acct_desc
        self.obj_desc = obj_desc
        self.acct_UCOA = acct_UCOA
        self.stepinfo = stepinfo
        
    def get_fund(self):
        return(self.fund)
            
    def get_acct(self):
        return(self.acct)
            
    def get_obj(self):
        return(self.obj)
            
    def get_position(self):
        return(self.position)
        
    def get_rate(self):
        return(self.rate)
            
    def get_earnings(self):
        return(self.earnings)
            
    def get_acct_desc(self):
        return(self.acct_desc)
            
    def get_obj_desc(self):
        return(self.obj_desc)
            
    def get_acct_UCOA(self):
        return(self.acct_UCOA)
    
    def get_stepinfo(self):
        return(self.stepinfo)
    
class Person():                                                #generic employee class
    def __init__(self,name):                                   #constructor
        self.name = name                                       #name
        self.person_id = None                                  #unique identifier
        self.payperiods = {}                                   #payperiod objects
        return
    
    def get_name(self):                                        #return name of person
        return(self.name)
    
    def get_payperiods(self):
        return(self.payperiods)
    
    def get_payperiod(self,school_year,seqno):
        try:
            return(self.payperiods[school_year][seqno])
        except IndexError:
            return({})
            
    def add_payperiod_by_index(self,syear,syseq,pperiod):        #payperiod school year and seqno
        if syear not in self.payperiods.keys():
            self.payperiods[syear] = {}
        if syseq not in self.payperiods[syear].keys():
            self.payperiods[syear][syseq] = pperiod
        return
    
class teacher_salary_matrix():
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
        
class UCOA_labels():
    def __init__(self):
        """ UCOA_labels class provides labels for UCOA fields"""
        self.labels = {}
    
        cols = ['Fund','Loc','Func','Prog','Sub','JC','Obj']
        descs = {'Fund':'Fund Description','Loc':'Location Description','Func':'Function Description', \
             'Prog':'Program Description','Sub':'Subject Description','JC':'Job Class Description', \
             'Obj':'Object Description'}
        for col in cols:
            self.labels[col] = {}

        for fyear in np.arange(2018,2009,-1):
            fm1 = fyear-1
            path = '../../finance_subcommittee/RIDE/UCOA_files/Expense_' + str(fm1) + '_' + str(fyear) + '.csv'
            df1 = pd.read_csv(path)
            df1['fyear'] = fyear
            fyear = fyear - 1
            if ('District ID' in df1.columns):
                df1 = df1.rename(columns={'District ID': 'Dist No'})
            if ('Object' in df1.columns):
                df1 = df1.rename(columns={'Object': 'Obj',\
                    'Revenue Object Description':'Object Description'})
            df1 = df1.loc[df1['Dist No']==90]

            dct = df1.to_dict(orient='list')
            for col in cols: 
                try:
                    for i in np.arange(len(dct[col])):
                        try:
                            code = int(dct[col][i])
                        except ValueError:
                            code = np.NaN
                        if (code==code):
                            if (code not in self.labels[col].keys()):
                                self.labels[col][code] = dct[descs[col]][i]
                except KeyError:
                    print("KeyError on ",col,path)
        return
    
    def get_labels_dictionary(self):
        """Returns the UCOA labels dictionary"""
        return(self.labels)
    
    def get_label(self,col,code):
        """Usage: get_label(col,code) returns the code for field col"""
        if (isinstance(code,str)):
            code = float(code)
        try:
            return(self.labels[col][code])
        except KeyError:
            return('No Label')
        
    
class scenario():                                              #scenario
    def __init__(self,sid,step,fte,payments,salary):           #constructor
        self.sid = sid                                         #identifier
        self.step = step                                       #step
        self.fte = fte                                         #fte
        self.payments = payments                               #payments
        self.salary = salary                                   #salary
        return
    
    def get_sid(self):                                         #return the identifier
        return(self.sid)
    
    def get_step(self):
        return(self.step)
    
    def get_fte(self):
        return(self.fte)
            
    def get_salary(self):
        return(self.salary)
            
    def get_payments(self):                          
        return(self.payments)