/**
 * =============
 * Dynamic list
 * =============
 * 
 * Implementation file for the general-purpose List class.
 */
#include <stdlib.h>
#include <stdio.h>

#include "random.h"
#include "list.h"

#define INITIAL_CAPACITY (3)
#define GROWTH_FACTOR (3/2.)



// ----- Main structure

// The structure is private and should not be accessed directly 
// from outside this file, but with the interface described in the 
// header file.
struct List_struct { /** 
    A dynamic list that, in principle could hold any data type.
    */
    void **content; // The list
    int capacity;// The capacity of the list
    int ocupancy;// The number of items currently in the list
};

typedef struct List_struct List;



// ----- Methods

List *List_new() { /**
    Create a new empty list with the given data type. 
    */
    // Create the list
    List *self = malloc(1 * sizeof(self));
    
    // Initialize the list
    int ocupancy = 0;
    int capacity = INITIAL_CAPACITY; 
    self->ocupancy = ocupancy;
    self->capacity = capacity;
    self->content = malloc(sizeof(void *) * capacity);
    
    return self;
    
} // --- List_new
 
List *List_del( List *self ) { /**
    Deleter for a dynamic list.
    */
    free(self->content);
    free(self);
} // --- List_del

int List_size( List *self ) { /**
    Return the number of items in the list.
    */
    return self->ocupancy;
    
} // --- List_size

List *List_grow_( List *self ) { /**
    Make more room.
    
    Increase the capacity by 3/2 of the current one.
    */
    int previous_capacity = self->capacity;
    
    int new_capacity = previous_capacity * GROWTH_FACTOR;
    
    self->content = realloc(self->content, sizeof(void *)*new_capacity);
    self->capacity = new_capacity;
    
    return self;
    
} // --- List_grow_

List *List_push( List *self, void *item ) { /**
    Add an element to the list.
    
    If needed, make more room.
    */
    
    // Check if reallocation is needed
    int current_items = self->ocupancy;
    int current_capacity = self->capacity;

    int needed_space = (current_items+1);
    if ( !(needed_space <= current_capacity) ) {
        
        // A reallocation is needed
        self = List_grow_(self);
    }

    // Add the item
    int next_index = current_items;
    self->content[ next_index ] = item;
    self->ocupancy += 1;
        
    return self;
    
} // --- List_push

void *List_at( List *self, int i ) { /**
    Find the item at the given index.
    
    If the index is not found, return NULL and warn.
    */
    void *item = NULL;
    
    if (0 <= i && i < List_size(self)) {
        item = self->content[i];
        
    } else {
        // OUT OF BOUNDS
        fprintf(stderr, 
                "Index %d out of bounds for list with %d items.\n",
                    i,
                    List_size(self));
    }
    
    return item;
    
} // --- List_at

void *List_pop( List *self) { /**
    Pop an item from the list.
    */
    int last_index = self->ocupancy - 1;
    
    void *last_item = List_at(self, last_index);
    
    self->ocupancy--; // The item is now out of the list.
    
    return last_item;
    
} // --- List_pop

void List_print( List *self, void(*print_item)(void *) ) { /**
    Print the list.
    
    The print_item parameter is a pointer function that handles
    the printing of each individual element.
    */
    printf("<List(capacity=%d, ocupancy=%d, content=[\n\t",
           self->capacity,
           self->ocupancy);
    
    for(int i=0; i < self->ocupancy; i++) {
        // Fetch item
        void *item = List_at(self, i);
        // Print item
        if (item) {
            (*print_item)(item);
        } else {
            printf("None");
        }
        
        printf(",\n\t");
    }
    printf("]>\n");
    
} // --- List_print

List *List_empty( List *self ) { /**
    Remove all items.
    */
    self->ocupancy = 0;
    return self;
    
} // --- List_empty

void *List_random_item( List *self ) { /**
    Return a random item.
    */
    // Select an index
    int i = (int)(random_float() * List_size(self));
    
    return List_at( self, i );
    
} // --- List_random_item


#undef INITIAL_CAPACITY
#undef GROWTH_FACTOR
