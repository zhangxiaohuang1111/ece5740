//========================================================================
// Unit tests for ubmark sort
//========================================================================

#include "ece4750.h"
#include "ubmark-sort.h"
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

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_2_sort_empty
//------------------------------------------------------------------------

void test_case_2_sort_empty()
{
  ECE4750_CHECK( L"test_case_2_sort_empty" );

  int a[] = {};
  ubmark_sort( a, 0 );

  ECE4750_CHECK_INT_EQ( is_sorted(a, 0), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_3_sort_one_element
//------------------------------------------------------------------------

void test_case_3_sort_one_element()
{
  ECE4750_CHECK( L"test_case_3_sort_one_element" );

  int a[] = { 42 };
  ubmark_sort( a, 1 );

  ECE4750_CHECK_INT_EQ( a[0], 42 );
  ECE4750_CHECK_INT_EQ( is_sorted(a, 1), 1 );
  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_4_sort_all_equal
//------------------------------------------------------------------------

void test_case_4_sort_all_equal()
{
  ECE4750_CHECK( L"test_case_4_sort_all_equal" );

  int a[]     = { 7, 7, 7, 7 };
  int a_ref[] = { 7, 7, 7, 7 };

  ubmark_sort( a, 4 );

  for ( int i = 0; i < 4; i++ )
    ECE4750_CHECK_INT_EQ( a[i] , a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_5_sort_with_negatives
//------------------------------------------------------------------------

void test_case_5_sort_with_negatives()
{
  ECE4750_CHECK( L"test_case_5_sort_with_negatives" );

  int a[]     = { -1, -3, -2, 0, 2 };
  int a_ref[] = { -3, -2, -1, 0, 2 };

  ubmark_sort( a, 5 );

  for ( int i = 0; i < 5; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

  ECE4750_CHECK_INT_EQ( ece4750_get_heap_usage(), 0 );
}

//------------------------------------------------------------------------
// test_case_6_sort_large_array
//------------------------------------------------------------------------

void test_case_6_sort_large_array()
{
  ECE4750_CHECK( L"test_case_6_sort_large_array" );

  int a[] = { 9, 7, 5, 3, 1, 8, 6, 4, 2, 0 };
  int a_ref[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };

  ubmark_sort( a, 10 );

  for ( int i = 0; i < 10; i++ )
    ECE4750_CHECK_INT_EQ( a[i], a_ref[i] );

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

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}
