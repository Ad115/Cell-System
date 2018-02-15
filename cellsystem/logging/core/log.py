class Log:
    "A logger class that registers certain actions."
    
    def __init__(self, *args, **kwargs):
        pass
    # ---
    
    def preparefor(self, actionname, *args, **kwargs):
        'Save previous state before the entity takes the given action.'
        getattr(self, 'preparefor_'+actionname)(*args, **kwargs)
    # ---
        
    def log(self, actionname, *args, **kwargs):
        'Log the action.'
        getattr(self, 'log_'+actionname)(*args, **kwargs)
    # ---
# ---Log
