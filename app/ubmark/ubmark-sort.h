//========================================================================
// ubmark-sort
//========================================================================
// This microbenchmark sorts an array of integers.

#ifndef UBMARK_SORT_H
#define UBMARK_SORT_H

// Declaration of the main sorting function
void ubmark_sort(int* x, int size);

// Helper function declarations
void swap(int* a, int* b);
int partition(int* array, int low, int high);
void quicksort(int* array, int low, int high);

#endif /* UBMARK_SORT_H */
