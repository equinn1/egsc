from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

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
    
    def get_eg_acct_codes6(self):
        """Returns dictionary of 6-digit account codes."""
        return(self.EG_account_codes6)
    