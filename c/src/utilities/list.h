/**
 * =============
 * Dynamic list
 * =============
 * 
 * Header defining the external interface for 
 * the general-purpose List class.
 */

#pragma once



// ----- Main structure

typedef struct List_struct List /** 
    A dynamic list that, in principle could hold any data type.
    */;

    

// ----- Methods

List *List_new() /**
    Create a new empty list with the given data type. 
    */;
 
List *List_del( List *self ) /**
    Deleter for a dynamic list.
    */;
    
int List_size( List *self  ) /**
    The number of items in the list.
    */;

List *List_push( List *self, void *item ) /**
    Add an element to the list.
    
    If needed, make more room.
    */;

void *List_at( List *self, int i ) /**
    Find the item at the given index.
    
    If the index is not found, return NULL and warn.
    */;

void *List_pop( List *self ) /**
    Pop an item from the list.
    */;

void List_print( List *self, void(*print_item)(void *) ) /**
    Print the list.
    
    The print_item parameter is a pointer function that handles
    the printing of each individual element.
    */;

List *List_empty( List *self ) /**
    Remove all items.
    */;
    
void *List_random_item( List *self ) /**
    Return a random item from the list.
    */;
