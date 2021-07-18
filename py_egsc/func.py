class Func():                                                            #generic UCOA Func class
    def __init__(self,func,func_description):                #constructor
        self.func      = func
        self.func_description = func_description
        return

    def get_func(self):
        return(self.func)
    
    def set_func(self,func):
        self.func = func
        return
            
    def get_func_description(self):
        return(self.func_description)
    
    def set_func_description(self,func_description):
        self.func_description = func_description
        return
