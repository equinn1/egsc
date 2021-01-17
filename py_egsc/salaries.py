from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd
    
class Teacher_salary():
    def __init__(self):         #constructor

        self.cba_cols ={'B': 0,'B+30': 1,'M': 2,'M+30': 3,'M2/CAGS': 4, 'D': 5}
        
        self.cols_cba ={0:'B',1:'B+30',2:'M',3:'M+30',4:'M2/CAGS',5:'D'}
        
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
        return            
    
    def get_cba_matrix(self):
        return(self.cba)
    
    def get_school_year_cba_matrix(self,school_year):
        return(self.cba[school_year])
    
    def get_salary(self,school_year,col,step):      #look up salary by year, column, step
        """Returns CBA salary given school year, column."""
      
        s  = int(step)-1                                 #step index is one less than the step number
        try: 
            c = self.cba_cols[col]                  #column within the CBA salary matrix
        except KeyError:
            print("Columns are B, B+30, M, M+30, M2/CAGS, D")
            return                                    
        
        try:
            sm = self.cba[school_year]
            return sm[s,c]            #look up the value if it exists
        except KeyError:                                        #otherwise raise error condition
            print("KeyError in get_salary: ",school_year,col,step)
        except IndexError:
            print("IndexError in get_salary: ",school_year,col,step)
        return
    
    def get_colname(self,col_index):              #look up column name from column index
        return(self.cols_cba(col_index)) 
    
class Para_rates():
    def __init__(self):         #constructor
    
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
        
    def get_school_year_cba_matrix(self,school_year):
        return(self.cba[school_year])

class Facilities_rates():
    def __init__(self):         #constructor
        
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

        
        #added stipend $650 November, 2018

            
    def get_cba_matrix(self):
        return(self.cba)
    
    def get_cba_matrix_by_year(self, school_year):
        return(self.cba[school_year])
    
    
    
