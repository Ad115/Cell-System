from .log import Log

class WeakLog(Log):
    'Ignore silently calls to not implemented log methods.'
    
    def preparefor(self, action, *args, **kwargs):
        try:
            logaction = getattr(self, 'preparefor_'+action)
        except AttributeError:
            return
        else:
            logaction(*args, **kwargs)
            
    def log(self, action, *args, **kwargs):
        try:
            logaction = getattr(self, 'log_'+action)
        except AttributeError:
            return
        else:
            logaction(*args, **kwargs)
