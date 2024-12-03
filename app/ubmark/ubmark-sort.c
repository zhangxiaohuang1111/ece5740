//========================================================================
// ubmark-sort
//========================================================================

#include "ubmark-sort.h"
#include <stddef.h>  // For NULL

//------------------------------------------------------------------------
// Helper function: swap
// Swaps two elements in an array
//------------------------------------------------------------------------
void swap(int* a, int* b) {
  int temp = *a;
  *a = *b;
  *b = temp;
}

//------------------------------------------------------------------------
// Helper function: partition
// Partitions the array and returns the pivot index
//------------------------------------------------------------------------
int partition(int* array, int low, int high) {
  int pivot = array[high];  // Choosing the last element as the pivot
  int i = low - 1;

  for (int j = low; j < high; j++) {
    if (array[j] < pivot) {
      i++;
      swap(&array[i], &array[j]);
    }
  }

  swap(&array[i + 1], &array[high]);
  return i + 1;
}

//------------------------------------------------------------------------
// Helper function: quicksort
// Recursive quicksort function to sort an array
//------------------------------------------------------------------------
void quicksort(int* array, int low, int high) {
  if (low < high) {
    int pivot_index = partition(array, low, high);
    quicksort(array, low, pivot_index - 1);
    quicksort(array, pivot_index + 1, high);
  }
}

//------------------------------------------------------------------------
// Main function: ubmark_sort
// Sorts an array of integers using quicksort
//------------------------------------------------------------------------
void ubmark_sort(int* x, int size) {
  // Handle edge cases
  if (x == NULL || size <= 1) {
    return;
  }

  // Call quicksort on the entire array
  quicksort(x, 0, size - 1);
}
