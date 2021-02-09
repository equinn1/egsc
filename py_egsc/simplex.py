from datetime import datetime, timedelta, date
import numpy as np
import pandas as pd

class Simplex():                                                            #generic check class
    def __init__(self,p=1.0,lbl='default',stype='default',fc=None):                #constructor
        self.simplex   = {1:{'p':p, 'lbl':lbl, 'fc':fc},'stype':stype}
        return

    def get_simplex(self):
        return(self.simplex)
    
    def add_element(self,prob):
        ix = len(self.simplex)
        for i in self.simplex.keys:
            self.simplex[i]['p'] = self.simplex[i]['p']*(1.0-prob)
        self.simplex[ix]['p'] = prob
        return
    
    def set_simplex(self,plex):
        self.simplex = plex
        return
            
    def get_label(self,ix):
        return(self.simplex[ix]['lbl'])
    
    def set_label(self,ix,lbl):
        self.simplex[ix]['lbl'] = lbl
        return
    
    def get_fc(self,ix):
        return(self.simplex[ix]['fc'])
    
    def set_fc(self,ix,fc):
        self.simplex[ix]['fc'] = fc
        return
            
    def get_p(self,ix):
        return(self.simplex[ix]['p'])
    
    def set_p(self,ix,prob):
        self.simplex[ix]['p'] = prob
        for i in self.simplex.keys():
            if (i != ix):
                self.simplex[i]['p'] = self.simplex[i]['p']*(1.0-prob)
        return
                
    def get_stype(self):
        return(self.simplex['stype'])
    
    def set_stype(self,stype):
        self.simplex['stype'] = stype
        return

