//========================================================================
// Unit tests for mtbmark-sort helper functions
//========================================================================

#include "ece4750.h"          // Include the provided unit test utilities
#include "mtbmark-sort.h"     // Include the header for the functions we are testing

//------------------------------------------------------------------------
// test_case_1_merge
//------------------------------------------------------------------------
// Test the merge function

void test_case_1_merge()
{
    ECE4750_CHECK(L"test_case_1_merge");

    int array[] = {1, 4, 7, 2, 5, 8}; // Two sorted subarrays: [1, 4, 7] and [2, 5, 8]
    int temp[6];

    merge(array, 0, 3, 6, temp);

    int expected[] = {1, 2, 4, 5, 7, 8};
    for (int i = 0; i < 6; i++) {
        ECE4750_CHECK_INT_EQ(array[i], expected[i]);
    }
}

//------------------------------------------------------------------------
// test_case_2_mtbmark_sort_small
//------------------------------------------------------------------------
// Test mtbmark_sort on a small array

void test_case_2_mtbmark_sort_small()
{
    ECE4750_CHECK(L"test_case_2_mtbmark_sort_small");

    int array[] = {4, 1, 3, 2};
    int expected[] = {1, 2, 3, 4};

    mtbmark_sort(array, 4);

    for (int i = 0; i < 4; i++) {
        ECE4750_CHECK_INT_EQ(array[i], expected[i]);
    }
}

//------------------------------------------------------------------------
// test_case_3_mtbmark_sort_large
//------------------------------------------------------------------------
// Test mtbmark_sort on a larger array

void test_case_3_mtbmark_sort_large()
{
    ECE4750_CHECK(L"test_case_3_mtbmark_sort_large");

    int array[] = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    int expected[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    mtbmark_sort(array, 10);

    for (int i = 0; i < 10; i++) {
        ECE4750_CHECK_INT_EQ(array[i], expected[i]);
    }
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------
// Main entry point for unit tests

int main(int argc, char** argv)
{
    __n = (argc == 1) ? 0 : ece4750_atoi(argv[1]);

    // Run all test cases
    if ((__n <= 0) || (__n == 1)) test_case_1_merge();
    if ((__n <= 0) || (__n == 2)) test_case_2_mtbmark_sort_small();
    if ((__n <= 0) || (__n == 3)) test_case_3_mtbmark_sort_large();

    ece4750_wprintf(L"\n\n");
    return ece4750_check_status;
}