 
/*
 * Simple program to demonstrate a couple uses for pointers. This program was
 * written so I could learn more about how to apply pointers and their syntax.
 * As I'm a C novice, please don't just take this file for granted as it may
 * contain errors and or bad practises.
 *
 * By Gerard (gerjo) Meier
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
 
// Some function prototypes as we're using a "One-pass compiler":
void pointersAndArrays(void);
void referencesAndVariables(void);
void referencesAndStructs(void);
void testingArrays(void);
void pointerToStruct(void);
void pointerToFunction(void);
void pointerToFunctionInStruct(void);
 
int  multiply(int a, int b);
int  add(int a, int b);
int* getArray1();
int* getArray2();
int* getArray3();
 
// Point of entry:
int main(int argc, char *argv[]) {
   
    printf("Testing pointers and arrays: \n --------------------\n");
    pointersAndArrays();
   
    printf("\n\n\nTesting references and variables: \n --------------------\n");
    referencesAndVariables();
   
    printf("\n\n\nTesting references and structs: \n --------------------\n");
    referencesAndStructs();
   
    printf("\n\n\nTesting Arrays: \n --------------------\n");
    testingArrays();
   
    printf("\n\n\nTesting Pointers to Structs: \n --------------------\n");
    pointerToStruct();
   
    printf("\n\n\nTesting Pointers to functions: \n --------------------\n");
    pointerToFunction();
   
    printf("\n\n\nTesting Pointers to functions within structs (fake classes?): \n --------------------\n");
    pointerToFunctionInStruct();
   
    system("PAUSE");   
    return 0;
}
 
// Demonstrate that an array is nothing more than a bunch of memory "blocks" in a row.
void pointersAndArrays(void) {
    int i;
    int array[] = {0,1,2,3,4,5,6,7,8,9};
    int *pointerToArray;
   
    pointerToArray = array; // Notice the lacking &, which apparently has to be ommitted when using arrays.
   
   
    for(i = 0; i < 10; ++i) {
        // Using an index is the same as incrementing the pointer address. (unsure how "safe" this actually is)
        assert(array[i] == *(pointerToArray + i));
       
        printf("Values:(%i == %i)  Addresses:(%i == %i)\n", array[i], *(pointerToArray + i), &array[i], (pointerToArray + i));
    }
}
 
// Reference two variables to hold the same "value"
void referencesAndVariables(void) {
    int value;
    int *pointerToValue;
   
    value            = 100;
    pointerToValue   = &value;
    value            = 99;
   
    // The address of value is the same as pointerToValue!
    assert(&value == pointerToValue);
    printf("%i == %i\n", &value, pointerToValue);
   
    // The values are the same, too.
    assert(value == *pointerToValue);
    printf("%i == %i\n", value, *pointerToValue);
}
 
// Reference a variable with in a struct:
void referencesAndStructs(void) {
 
    int value;      // Some value that we'll be playing with.
    struct Wrapper; // Forward declaration.
 
    // Create some structure:
    struct Wrapper {
        int *pointerToValue;      
    } foo;
   
    // "link" the pointer to the actual int:
    foo.pointerToValue = &value; // The & makes sure we retrieve the memory address, not the memory value.
                                 // notice the lacking * as we're setting the actual memory address, not memory value.
   
    // Assign some values to both variables:
    *foo.pointerToValue = 102;  // Notice the * is used this time to access the actual memory value, and not the memory address.
    value = 78;                 // Set the original variable.
   
    // Variables hold the same data!
    assert(value == *foo.pointerToValue);
    printf("%i == %i\n", value, *foo.pointerToValue);
}
 
 // This is how it should NOT be done. It will "probably" compile just fine,
 // and "may" execute too, if you're "lucky".
int* getArray1(void) {
    int array[] = {0,1,2,3,4,5,6,7,8,9}; // Privately allocated array.
   
    // Return a pointer to a privately allocated array is not "allowed":
    return array; // Will mostlikely yield a compiler "warning", not an "error".
}
 
// This is the right idea, however, sooner or later we might cause a buffer
// overflow and override some vital part in the memory. The memory I believe is also
// privately "allocated".
// In short: This is NOT how it should be done.
int* getArray2(void) {
    int *array;
    int i;
     
    // We just "assume" that the next 9 memory blocks are free, while this will
    // probably "work" most of the time, it's best to first actually allocate the
    // memory (as seen in the next function)
    for(i = 0; i < 10; ++i) array[i] = i;
   
    return array;
}
 
// This is how it should be done. Much like the C++ new keyword, the
// memory has to be released after use via the "free(*pointer)" function. (called delete/delete[] in C++)
int* getArray3(void) {
    int *array = (int*)malloc(10 * sizeof (int));  // Dynamically allocate memory (array)
    int i;
   
    if(array == NULL) abort();// The computer ran out of memory? Probably want to abort the program here.
   
    // Fill the array:
    for(i = 0; i < 10; ++i) array[i] = i;
   
    // Do not forget to eventually release the memory, too!
    return array;
}
 
void testingArrays(void) {
    //int* array1 = getArray1(); // This will probably crash the application, or otherwise cause unexpected behavior.
    //int* array2 = getArray2(); // This will probably crash the application, or otherwise cause unexpected behavior.
    int* array3 = getArray3();   // The only correct function to return an int[10] array
    int i;
   
    for(i = 0; i < 10; ++i) {
        assert(i == array3[i]);  
       
        // Notice how variable i remains at the same memory address!
        printf("Values:(%i == %i)  Addresses:(%i != %i)\n", i, array3[i], &i, &array3[i]);
 
    }
   
    // No memory leak in this awesome application!
    free(array3);
}
 
void pointerToStruct(void) {
    // Define some basic structure:
    struct someStruct {
        int a;
    } myStruct;
   
    //struct someStruct myStruct;
    struct someStruct *pointerToStruct;
   
    pointerToStruct     = &myStruct; // Point the pointer towards the actual struct instance.
    pointerToStruct->a  = 101; // Set "a" via the pointer. (notice the -> instead of .)
    myStruct.a          = 102; // or set "a" directly. (notice the . instead of ->)
   
    assert(myStruct.a == pointerToStruct->a);
    printf("%i == %i\n", myStruct.a, pointerToStruct->a);
}
 
 
int multiply(int a, int b) {
    return a * b;  
}
 
int add(int a, int b) {
    return a + b;  
}
 
void pointerToFunction(void) {
    // pointer to function, notice how the return types and arguments are definend.
    int (*pointerToFunction) (int, int) = &multiply;
   
    assert(multiply(3, 3) == pointerToFunction(3, 3));
    //printf("%i == %i\n", multiply(3, 3), pointerToFunction(3, 3));
    printf("Values:(%i == %i)  Addresses:(%i == %i)\n", multiply(3, 3), pointerToFunction(3, 3), &multiply, pointerToFunction);
}
 
// Fancy that! functions in a struct:
void pointerToFunctionInStruct(void) {
    // A simple wrapper struct for some "math" tools:
    struct MathTools {
        int (*multiply) (int, int);
        int (*add) (int, int);
    } tools;
 
    // Point the pointers towards the functions:
    tools.multiply = &multiply;
    tools.add      = &add;
   
    // Assertions:
    assert(tools.multiply(3, 3) == tools.add(6, 3));
    printf("%i %i\n", tools.multiply(3, 3), tools.add(6, 3));
}
