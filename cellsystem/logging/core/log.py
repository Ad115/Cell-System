class Log:
    """The base for logger classes that trigger when
    certain actions are performed.
    
    """
    
    def __init__(self, *args, **kwargs):
        self.silenced = False
    # ---
    
    def silence(self):
        "Silence/deactivate log temporarily."
        self.silenced = True
    # ---
    
    def activate(self):
        "Activate the log if deactivated."
        self.silenced = False
    # ---
    
    def preparefor(self, actionname, *args, **kwargs):
        'Save previous state before the entity takes the given action.'
        if not self.silenced:
            getattr(self, 'preparefor_'+actionname)(*args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        if not self.silenced:
            getattr(self, 'log_'+actionname)(*args, **kwargs)
    # ---
# ---Log
