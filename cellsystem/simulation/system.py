"""

System-related classes.

This module defines a general system that can be used as
the base of a computation graph.

A system is composed of entities and interactions btw them,
it coordinates all processes.

"""

import collections


class Entity:
    '''An entity is something that resides in the system.

    It processes information according to it's internal state 
    and the information flowing through the links it shares with 
    other entities.
    
    An entity registers the following methods:
        - process(time)
    '''
    def __init__(self):
        self.state = None
    
    def process(self, time):
        pass
# --- Entity


class Interaction:
    'A structure representing flow of information btw entities.'
    
    def __init__(self, entities, effect):
        self.entities = entities
        self.effects = [effect]
        
    def append(self, effect):
        'Effects btw the same entities can be appended and executed in order'
        self.effects.append(effect)
        
    def process(self):
        'Executes the interaction.'
        for effect in self.effects:
            effect(*self.entities)
# --- Interaction


'Representing an isolated process.'
Process = collections.namedtuple('Process', ['entities', 'effects'])
# --- Process


class System:
    """
    The global system and event dispatcher.

    Aware of the passage of time (steps). A system is 
    composed of entities and interactions between them,
    at each time step, the system triggers the proceses 
    associated with them.

    """

    def __init__(self, *args, **kwargs):
        'Initialize an empty system.'
        self.entities = set()
        self.procesable = set()
        self.toentity = {}
        self.toentityname = {}
        
        self.interactions = {}
        self.time = None
        
        self.inithooks = {}
        self.prehooks = {}
        self.hooks = {}
    # ---
    
    def __getitem__(self, entityname):
        'Access the entities by name.'
        return self.toentity[entityname]
    # ---

    def add_entity(self, entity, name, procesable=True, inithook=None):
        """Add an entity to the graph.
        
        If procesable, the entity.process(time) method is called 
        on each time step.
        
        Inithooks are callables called at initialization.
        
        """
        self.entities.add(entity)
        if procesable:
            self.procesable.add(entity)
        self.toentity[name] = entity
        self.toentityname[entity] = name
        # Process hooks
        if inithook:
            self.add_interaction_to(self.inithooks,
                                    inithook, 
                                    [name])
    # ---
    
    def process_interactions_in(self, interactions):
        'From the dict-like container of interactions, process items.'
        for interaction in interactions.values():
            interaction.process()
    # ---
        
    def step(self):
        'Take a single step forward in time.'
        # Process pre-step hooks
        self.process_interactions_in(self.prehooks)
        
        # Process linked items
        self.process_interactions_in(self.interactions)
        # Process each entity
        for entity in self.procesable:
            entity.process(self.time)
            
        # Process post-step hooks
        self.process_interactions_in(self.hooks)
        
        self.time += 1
    # ---
         
    def start(self):
        'Initialize things before starting simulation.'
        # Init time
        if self.time is None:
            self.time = 0
        # Make the initialization actions
        self.process_interactions_in(self.inithooks)
    # ---
    
    def update_hooks(self, hooktype, newhooks):
        'Add the given hooks to the system.'
        if newhooks:
            for hook in newhooks:
                self.add_interaction_to(hooktype, hook.effects, hook.entities)
    # ---
         
    def run(self, steps, init=None, after_step=None, before_step=None):
        'Start running the simulation.'
        # Handle hooks
        self.update_hooks(self.inithooks, init)
        self.update_hooks(self.hooks, after_step)
        self.update_hooks(self.prehooks, before_step)
        
        # Make sure things are initialized
        self.start()
        
        # Take steps
        for _ in range(steps):
            self.step() 
    # ---
    
    def stateof(self, entityname):
        "Ask the entity for it's state"
        return self[entityname].state
    # ---
    
    def link(self, effect, entitynames):
        'Add an interation btw named entities.'
        self.add_interaction_to(self.interactions,
                                effect, 
                                entitynames)
    # ---
    
    def add_interaction_to(self, container, effect, entitynames):
        'Add an interaction btw named entities to a dict-like container.'
        entities = tuple(self.toentity[ename] 
                                for ename in entitynames)
        
        # Check if there is already some link btw
        # those same entities.
        if entities in container:
            # Add the new effect
            container[entities].append(effect)
            
        else:
            # Else, add the new link
            interaction = Interaction(entities, effect)
            container[entities] = interaction
    # ---
# --- System
