//========================================================================
// Unit tests for mtbmark sort
//========================================================================

#include "ece4750.h"
#include "mtbmark-sort.h"
#include "ubmark-sort.dat"

//------------------------------------------------------------------------
// is_sorted
//------------------------------------------------------------------------
// Helper function that returns 1 if sorted and 0 if unsorted

int is_sorted( int* x, int n )
{
  for ( int i = 0; i < n-1; i++ ) {
    if ( x[i] > x[i+1] )
      return 0;
  }
  return 1;
}

//------------------------------------------------------------------------
// test_case_1_sort_basic
//------------------------------------------------------------------------

void test_case_1_sort_basic()
{
  ECE4750_CHECK( L"test_case_1_sort_basic" );

  int a[]     = { 4, 3, 6, 5 };
  int a_ref[] = { 3, 4, 5, 6 };

  mtbmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted( a, 4 ), 1 );
}

//------------------------------------------------------------------------
// test_case_2_sort_empty
//------------------------------------------------------------------------

void test_case_2_sort_empty()
{
  ECE4750_CHECK( L"test_case_2_sort_empty" );

  int a[] = {};
  mtbmark_sort( a, 0 );

  ECE4750_CHECK_INT_EQ( is_sorted( a, 0 ), 1 );
}

//------------------------------------------------------------------------
// test_case_3_sort_one_element
//------------------------------------------------------------------------

void test_case_3_sort_one_element()
{
  ECE4750_CHECK( L"test_case_3_sort_one_element" );

  int a[] = { 42 };
  mtbmark_sort( a, 1 );

  ECE4750_CHECK_INT_EQ( a[0], 42 );
  ECE4750_CHECK_INT_EQ( is_sorted( a, 1 ), 1 );
}

//------------------------------------------------------------------------
// test_case_4_sort_all_equal
//------------------------------------------------------------------------

void test_case_4_sort_all_equal()
{
  ECE4750_CHECK( L"test_case_4_sort_all_equal" );

  int a[] = { 7, 7, 7, 7 };
  mtbmark_sort( a, 4 );

  ECE4750_CHECK_INT_EQ( is_sorted( a, 4 ), 1 );
}

//------------------------------------------------------------------------
// test_case_5_sort_with_negatives
//------------------------------------------------------------------------

void test_case_5_sort_with_negatives()
{
  ECE4750_CHECK( L"test_case_5_sort_with_negatives" );

  int a[]     = { -1, -3, -2, 0, 2 };
  int a_ref[] = { -3, -2, -1, 0, 2 };

  mtbmark_sort( a, 5 );

  for ( int i = 0; i < 5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted( a, 5 ), 1 );
}

//------------------------------------------------------------------------
// test_case_6_sort_large_array
//------------------------------------------------------------------------

void test_case_6_sort_large_array()
{
  ECE4750_CHECK( L"test_case_6_sort_large_array" );

  int a[]     = { 9, 7, 5, 3, 1, 8, 6, 4, 2, 0 };
  int a_ref[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };

  mtbmark_sort( a, 10 );

  for ( int i = 0; i < 10; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted( a, 10 ), 1 );
}

//------------------------------------------------------------------------
// test_case_7_sort_with_duplicates
//------------------------------------------------------------------------

void test_case_7_sort_with_duplicates()
{
  ECE4750_CHECK( L"test_case_7_sort_with_duplicates" );

  int a[] = { 3, 1, 2, 2, 3, 1 };
  int a_ref[] = { 1, 1, 2, 2, 3, 3 };

  mtbmark_sort( a, 6 );

  for ( int i = 0; i < 6; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( is_sorted( a, 6 ), 1 );
}

//------------------------------------------------------------------------
// test_case_8_sort_random
//------------------------------------------------------------------------

void test_case_8_sort_random() {
    ECE4750_CHECK( L"test_case_8_sort_random" );

    ece4750_srand(42); // Seed for reproducibility
    int n = 50; // Random array size
    int a[50];
    
    for ( int i = 0; i < n; i++ ) {
        int rand_value = ece4750_rand();  // Compute random value first
        while (rand_value >= 100) {      // Emulate mod operation for range 0-99
            rand_value -= 100;          // Subtract until in range
        }
        a[i] = rand_value;              // Assign value to array
    }

    mtbmark_sort( a, n );

    ECE4750_CHECK_INT_EQ( is_sorted(a, n), 1 );
    ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_9_sort_large_scale
//------------------------------------------------------------------------

void test_case_9_sort_large_scale() {
    ECE4750_CHECK( L"test_case_9_sort_large_scale" );

    int n = 100;
    int* a = ece4750_malloc( n * (int)sizeof(int) );
    for ( int i = 0; i < n; i++ )
        a[i] = n - i; // Reverse order

    mtbmark_sort( a, n );

    ECE4750_CHECK_INT_EQ( is_sorted(a, n), 1 );
    ece4750_free(a);
    ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1 ) ) test_case_1_sort_basic();
  if ( (__n <= 0) || (__n == 2 ) ) test_case_2_sort_empty();
  if ( (__n <= 0) || (__n == 3 ) ) test_case_3_sort_one_element();
  if ( (__n <= 0) || (__n == 4 ) ) test_case_4_sort_all_equal();
  if ( (__n <= 0) || (__n == 5 ) ) test_case_5_sort_with_negatives();
  if ( (__n <= 0) || (__n == 6 ) ) test_case_6_sort_large_array();
  if ( (__n <= 0) || (__n == 7 ) ) test_case_7_sort_with_duplicates();
  if ( (__n <= 0) || (__n == 8 ) ) test_case_8_sort_random();
  if ( (__n <= 0) || (__n == 9 ) ) test_case_9_sort_large_scale();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}