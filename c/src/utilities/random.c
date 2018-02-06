/**
 * =========
 * Random
 * =========
 * 
 * Implementation file for the random module.
 */
// The naming convention represents that the current module
// is called random, and the functions in the module have as names
// <module name>_<function name>

#pragma once

#include <stdlib.h>
#include <time.h>

#include "random.h"


void random_seed() { /**
    Inicializa el generador de números aleatorios
    */
    srand48(time(0));
    
} // --- random_seed

float random_float() { /**
    Get a random float between 0 and 1
    */
    return drand48();

} // --- random_float

int random_trial( float selector ) { /**
    Choose randomly true or false according to the selector.
    */
    float r = random_float();
    
    return r < selector;
    
} // --- random_trial
