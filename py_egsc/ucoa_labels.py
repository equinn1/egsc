import pickle

class UCOA_labels():
    def __init__(self):
        """ UCOA_labels class provides labels for UCOA fields"""
        
        with open('../../finance_subcommittee/UCOA_labels.pkl', 'rb') as handle:
            self.labels =  pickle.load(handle)
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