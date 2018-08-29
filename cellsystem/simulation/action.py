from numpy import random as rnd

class Action:
    """Objects of this class represent actions with an 
    associated probability.
    
    A complex action (with several arguments) can be executed
        by passing the arguments to the ``try_action`` method::
            
            >>> def complex_fn(a,b,c,d): return a,b,c,d
            

            >>> action = Action(a_func, probability=1)

            # Arguments are passed to `complex_fn`
            >>> action.try_action(1,2,3,4)
            (1,2,3,4)
                    
        The probability can be specified in several ways. 
        One of them is by giving a numeric value::
        
            # The procedure
            >>> def a_func(): pass
            
            >>> action = Action(a_func, probability=0.5)
            
            # The procedure will be executed ~50% of the times
            >>> action.try_action()
            
        Also, a function with no parameters will do the job::
        
            >>> action = Action(a_func, 
            ...                 probability=lambda : 0.5)
            
            # The procedure will be executed ~50% of the times
            >>> action.try_action()
            
        For more complex probabilities, one must specify the 
        desired probability to ``try_action``::
        
            >>> def complex_prob(a,b,c,d): return 0.5
            

            >>> action = Action(a_func, complex_prob)

            # Calculate the probability
            >>> p = action.probability(1,2,3,4)
            
            >>> action.try_action(probability=p)            
    """

    def __init__(self, action, probability=None, name=None):
        """
        Params:
        
            action (function): The procedure to be executed.
            
            probability (optional numeric or function):
                    The numeric probability or probability function.
                    Default is 1 (do always).
            
        """
        if probability is None:
            probability = 1
        
        self.action = action
        self.probability = probability
        self.name=name
    # ---
    
    def __repr__(self):
        return "{}(action={},probability={},name={})".format(self.__class__.__name__,
                                                             self.action,
                                                             self.probability,
                                                             self.name)
    # ---
    
    def __str__(self):
        return self.name
    # ---
    
    def __call__(self, *args, **kwargs):
        """Equivalent to calling ``try_action(*args, **kwargs)``."""
        return self.action(*args, **kwargs)
    # ---

    def try_action(self, *args, probability=None, **kwargs):
        """Perform the action according to it's probability."""
        if probability is None:
            try:
                # Check if a probability function was given
                probability = self.probability()
            except TypeError:
                # A numeric value vas given
                probability = self.probability
            
        if rnd.random() < probability:
            return self.action(*args, **kwargs)
    # ---
# --- Action
