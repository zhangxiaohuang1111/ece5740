//========================================================================
// mtbmark-sort
//========================================================================
#include "mtbmark-sort.h"
#include "ece4750.h"
#include "ubmark-sort.h"

//------------------------------------------------------------------------
// arg_t
//------------------------------------------------------------------------
// This is used to pass arguments when we spawn work onto the cores.

typedef struct {
  int* array; // Pointer to array
  int start;  // Start index
  int end;    // End index (exclusive)
} arg_t;

//------------------------------------------------------------------------
// Partition function
//------------------------------------------------------------------------

int partition(int* array, int start, int end) {
  int pivot = array[end - 1];
  int i = start - 1;
  for (int j = start; j < end - 1; j++) {
    if (array[j] <= pivot) {
      i++;
      int temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }
  int temp = array[i + 1];
  array[i + 1] = array[end - 1];
  array[end - 1] = temp;
  return i + 1;
}

//------------------------------------------------------------------------
// Quick Sort function
//------------------------------------------------------------------------

void quick_sort(int* array, int start, int end) {
  if (start < end) {
    int pivot = partition(array, start, end);
    quick_sort(array, start, pivot);
    quick_sort(array, pivot + 1, end);
  }
}

//------------------------------------------------------------------------
// Worker function
//------------------------------------------------------------------------

void work(void* arg_vptr) {
  arg_t* arg = (arg_t*)arg_vptr;
  quick_sort(arg->array, arg->start, arg->end);
}

//------------------------------------------------------------------------
// mtbmark_sort
//------------------------------------------------------------------------

void mtbmark_sort(int* x, int size) {
  // Divide the array into four parts
  int block_size = size / 4;

  // Create arguments for each part
  arg_t arg0 = {x, 0, block_size};
  arg_t arg1 = {x, block_size, 2 * block_size};
  arg_t arg2 = {x, 2 * block_size, 3 * block_size};
  arg_t arg3 = {x, 3 * block_size, size};

  // Spawn threads for sorting
  ece4750_bthread_spawn(1, &work, &arg1);
  ece4750_bthread_spawn(2, &work, &arg2);
  ece4750_bthread_spawn(3, &work, &arg3);

  // Core 0 sorts its part
  work(&arg0);

  // Wait for all threads to finish
  ece4750_bthread_join(1);
  ece4750_bthread_join(2);
  ece4750_bthread_join(3);

  // Merge sorted parts
  quick_sort(x, 0, size); // Final single-threaded merge sort
}