from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class UCOA_labels():
    def __init__(self):
        """ UCOA_labels class provides labels for UCOA fields"""
        self.labels = {}
    
        cols = ['Fund','Loc','Func','Prog','Sub','JC','Obj']
        descs = {'Fund':'Fund Description','Loc':'Location Description', \
                 'Func':'Function Description', \
                 'Prog':'Program Description', \
                 'Sub':'Subject Description', \
                 'JC':'Job Class Description', \
                 'Obj':'Object Description'}
        for col in cols:
            self.labels[col] = {}

        for fyear in np.arange(2018,2009,-1):
            fm1 = fyear-1
            path = '../../finance_subcommittee/RIDE/UCOA_files/Expense_' \
                + str(fm1) + '_' + str(fyear) + '.csv'
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