//========================================================================
// Unit tests for ubmark-sort helper functions
//========================================================================

#include "ece4750.h"          // Include the provided unit test utilities
#include "ubmark-sort.h"      // Include the header for the functions we are testing

//------------------------------------------------------------------------
// test_case_1_swap
//------------------------------------------------------------------------
// Test the swap function

void test_case_1_swap()
{
  ECE4750_CHECK( L"test_case_1_swap" );

  int a = 5;
  int b = 10;

  swap(&a, &b);

  // After swap, a should be 10 and b should be 5
  ECE4750_CHECK_INT_EQ(a, 10);
  ECE4750_CHECK_INT_EQ(b, 5);
}

//------------------------------------------------------------------------
// test_case_2_partition
//------------------------------------------------------------------------
// Test the partition function

void test_case_2_partition()
{
  ECE4750_CHECK( L"test_case_2_partition" );

  int array[] = {4, 3, 6, 1, 7};
  int pivot_index = partition(array, 0, 4);

  // Pivot index should separate the array such that all elements before it
  // are less than or equal to pivot, and all elements after it are greater.
  for (int i = 0; i < pivot_index; i++) {
    ECE4750_CHECK_TRUE(array[i] <= array[pivot_index]);
  }
  for (int i = pivot_index + 1; i <= 4; i++) {
    ECE4750_CHECK_TRUE(array[i] > array[pivot_index]);
  }
}


//------------------------------------------------------------------------
// test_case_3_quicksort
//------------------------------------------------------------------------
// Test the quicksort function

void test_case_3_quicksort()
{
  ECE4750_CHECK( L"test_case_3_quicksort" );

  int array[] = {4, 3, 6, 1, 7};
  int sorted_array[] = {1, 3, 4, 6, 7};

  quicksort(array, 0, 4);

  for (int i = 0; i < 5; i++) {
    ECE4750_CHECK_INT_EQ(array[i], sorted_array[i]);
  }
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  // Run all test cases
  if ( (__n <= 0) || (__n == 1 ) ) test_case_1_swap();
  if ( (__n <= 0) || (__n == 2 ) ) test_case_2_partition();
  if ( (__n <= 0) || (__n == 3 ) ) test_case_3_quicksort();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}
