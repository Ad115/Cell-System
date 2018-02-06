/**
 * =========
 * Random
 * =========
 * 
 * Utilities for randomness.
 */
// The naming convention represents that the current module
// is called random, and the functions in the module have as names
// <module name>_<function name>

#pragma once


// -------- Functions 

void random_seed() /**
    Inicializa el generador de números aleatorios
    */;

float random_float() /**
    Get a random float between 0 and 1
    */;

int random_trial( float selector ) /**
    Choose randomly true or false according to the selector.
    */;
