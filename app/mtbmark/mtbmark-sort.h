//========================================================================
// mtbmark-sort
//========================================================================
// This microbenchmark sorts an array of integers using a multi-threaded
// approach. It provides the main sort function and associated helpers.

#ifndef MTBMARK_SORT_H
#define MTBMARK_SORT_H

#include <stddef.h> // For size_t

// ----------------------------------------------------------------------
// mtbmark_sort
// ----------------------------------------------------------------------
// Multi-threaded sorting function.
//
// Parameters:
// - x    : Pointer to the integer array to be sorted.
// - size : Size of the array.
//
// The function uses multi-threading to divide the array into multiple
// blocks, sort each block in parallel, and merge the results.
void mtbmark_sort(int* x, int size);

// ----------------------------------------------------------------------
// Helper functions
// ----------------------------------------------------------------------

// Swap two integers in place
void swap(int* a, int* b);

// Partition the array around a pivot for quicksort
int partition(int* array, int low, int high);

// Perform quicksort on the array
void quicksort(int* array, int low, int high);

// Merge two sorted subarrays
void merge(int* array, int start, int mid, int end, int* temp);

// Worker function for multi-threaded sorting
void work(void* arg_vptr);

// ----------------------------------------------------------------------
// Data types
// ----------------------------------------------------------------------

// Struct for passing arguments to worker threads
typedef struct {
    int* array;  // Pointer to the array
    int start;   // Start index of the subarray
    int end;     // End index of the subarray
} arg_t;

#endif /* MTBMARK_SORT_H */