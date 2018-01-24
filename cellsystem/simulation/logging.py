"""

Logging capabilities for entities.

The decorator defined here serves as an interface with the 
logging classes.

It assumes a log has `preparefor` and `log` methods.

"""

from functools import wraps

def logged(action_name, prepare=True):
    """Decorate an action with logging.
    
    Allows to specify if a prelogging action is called.
    """
    # Real decorator
    def add_logging(action):
        # Decorated
        @wraps(action)
        def logged_action(self, *args, log=None, **kwargs):
            if log and prepare:
                log.preparefor(action_name, self)
                
            result = action(self, *args, **kwargs)
            
            if log:
                log.log(action_name, result)
                
            return result
        # ---
        return logged_action
    return add_logging
# ---