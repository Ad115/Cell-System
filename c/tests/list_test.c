 
/**
Dynamic list utilities test
-----------------------------

The module "list.h" contains functions and structures 
for hopefully pain-free handling of dynamic lists.
This is a test suite to ensure everything is OK.
*/

#include <stdio.h>
#include "../src/utilities/list.h"
#include "../src/utilities/random.h"

void print_int(void *item) {
    int real_item = *(int*)item;
    printf("%d", real_item);
}


int main() {


void print_string(void *item) {
    char *real_item = *(char**)item;
    printf("\"%s\"", real_item);
}
    List *a, *b;
    

    // --> testing List_new

    printf("\nTesting List_new:\n");
    
    a = List_new();
    b = List_new();
    
    // Try to print the empty arrays
    List_print(a, &print_int);
    List_print(b, &print_string);
    
    
    // --> testing List_push

    printf("\nTesting List_push:\n");
    int i=0;
    int j=1;
    int k=2;
    int l=3;
    int m=4;
    List_push(a, &i);
    List_print(a, &print_int);
    List_push(a, &j);
    List_push(a, &k);
    List_push(a, &l);
    List_print(a, &print_int);
    List_push(a, &m);
    List_print(a, &print_int);
    
    
    char *str = "Hello world!";
    List_push(b, &str);
    List_print(b, &print_string);
    char *str2 = "Hello motto";
    List_push(b, &str2);
    List_print(b, &print_string);
 
    
    // --> testing List_size
    
    printf("\nTesting List_size:\n");
    
    printf("The integer list has %d entries.\n", List_size(a));
    
    printf("The strings list has %d entries.\n", List_size(b));
    
    
    // --> testing List_at
    
    printf("\nTesting List_at:\n");
    
    int ii = *(int *)List_at(a,3);
    printf("The integer list at position 3 has: %d (must be a 3)\n", ii);
    
    char *sec = *(char **)List_at(b, 1);
    printf("The second entry on the strings list is: \"%s\" (must be \"Hello motto\")\n", sec);
    
    printf("If an out of bounds access is attempted,"
           " a warning is ensued and a null entry is returned: %p\n", List_at(b, 4));
   
    
    
    // --> testing List_random_item
    
    printf("\nTesting List_random_item:\n");
    
    // Seed the random number generator
    random_seed();
    
    printf("Two random entries from the integer list: %d, %d\n", *(int*)List_random_item(a), *(int*)List_random_item(a));
    
    printf("A random entry from the strings list: %s \n", *(char**)List_random_item(b));
    
    
    
    // --> testing List_pop
    
    printf("\nTesting List_pop:\n");
    
    int jj = *(int *)List_pop(a);
    printf("The integer list at the last position was: %d (must be a 4)\n", jj);
    printf("The list now contains the following...");
    List_print(a, &print_int);
    
    char *las = *(char **)List_pop(b);
    printf("The string list at the last position was: %s (must be \"Hello motto\")\n", las);
    printf("The list now contains the following...");
    List_print(b, &print_string);
    
    
    
    // --> testing List_empty
    
    printf("\nTesting List_empty:\n");
    
    List_empty(a);
    printf("The list of integers has been emptied...\n");
    List_print(a, &print_int);
    printf("Attempting access to the data...\n");
    List_at(a, 0);
    
    List_empty(b);
    printf("The list of strings has been emptied...\n");
    List_print(b, &print_string);
    printf("Attempting access to the data...\n");
    List_at(b, 0);
    
    
    // --> testing List_del
    
    printf("\nTesting List_del:\n");
    
    List_del(a);
    List_del(b);
}
    
