class Prog():                                                            #UCOA Prog class
    def __init__(self,prog,prog_description):                
        self.prog      = prog
        self.prog_description = prog_description
        return

    def get_prog(self):
        return(self.prog)
    
    def set_prog(self,prog):
        self.prog = prog
        return
            
    def get_prog_description(self):
        return(self.prog_description)
    
    def set_prog_description(self,prog_description):
        self.prog_description = prog_description
        return
