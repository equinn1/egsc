class Position():                                                            #generic position class
    def __init__(acct,obj,start_syear,years=1,fund='10000000',prog='10',init_person=None,func=None,jc=None,sub=None):
        self.fund           =      fund
        self.prog           =      prog
        self.start_syear    =      start_syear
        self.nyears         =      nyears
        self.init_person    =      init_person
        self.acct           =      acct
        self.obj            =      obj
        self.func           =      func
        self.jc             =      jc
        self.sub            =      sub
        return

    def get_fund(self):
        return(self.fund)
    
    def set_fund(self,fund):
        self.fund = fund
        return
    
    def get_nyears(self):
        return(self.nyears)
    
    def set_nyears(self,nyears):
        self.nyears = nyears
        return
    
    def get_sub(self):
        return(self.sub)
    
    def set_sub(self,sub):
        self.sub = sub
        return
    
    def get_prog(self):
        return(self.prog)
    
    def set_prog(self,prog):
        self.prog = prog
        return

    def get_start_syear(self):
        return(self.start_syear)
    
    def set_start_syear(self,start_syear):
        self.start_syear = start_syear
        return

    def get_acct(self):
        return(self.acct)
    
    def set_acct(self,acct):
        self.acct = acct
        return
    
    def get_end_syear(self):
        return(self.end_syear)
    
    def set_end_syear(self,end_syear):
        self.end_syear = end_syear
        return
    
    def get_init_person(self):
        return(self.init_person)
    
    def set_init_person(self,name):
        self.init_person = name
        return
    
    def get_obj(self):
        return(self.obj)
    
    def set_obj(self,obj):
        self.obj = obj
        return
    
    def get_jc(self):
        return(self.jc)
    
    def set_jc(self,jc):
        self.jc = jc
        return