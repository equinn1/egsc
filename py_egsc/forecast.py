from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Forecast():                                                            #generic check class
    def __init__(self,syear,sseq,itm):                #constructor
        self.syear = syear
        self.sseq  = sseq
        self.fund = itm.get_fund()
        self.acct = itm.get_acct()
        self.obj  = itm.get_obj()
        self.amt  = itm.get_earnings()
        self.simplex = Simplex()
        return

    def get_simplex(self):
        return(self.simplex)
    
    def get_fund(self):
        return(self.fund)
    
    def set_fund(self,fund):
        self.fund = fund
        return
    
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
    
    def set_simplex(self,plex):
        self.simplex = plex
        return