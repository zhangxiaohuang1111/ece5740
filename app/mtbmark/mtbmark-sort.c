#include "ece4750.h"
#include "ubmark-sort.h"
#include <stddef.h>

#define NUM_CORES 4
#define THRESHOLD 1000

typedef struct {
    int* array;
    int start;
    int end;
} arg_t;

void merge(int* array, int start, int mid, int end, int* temp) {
    int i = start, j = mid, k = 0;
    while (i < mid && j < end) {
        if (array[i] <= array[j])
            temp[k++] = array[i++];
        else
            temp[k++] = array[j++];
    }
    while (i < mid)
        temp[k++] = array[i++];
    while (j < end)
        temp[k++] = array[j++];
    for (int p = 0; p < k; p++)
        array[start + p] = temp[p];
}

void work(void* arg_vptr) {
    arg_t* arg = (arg_t*)arg_vptr;
    ubmark_sort(arg->array + arg->start, arg->end - arg->start);
}

void mtbmark_sort(int* x, int size) {
    if (!x || size <= 1) return;

    int block_size = size / NUM_CORES;

    // Calculate sizes and safely cast to int
    int arg_size = (int)(NUM_CORES * sizeof(arg_t));
    int temp_size = (int)((size_t)size * sizeof(int));

    // Allocate memory using ece4750_malloc
    arg_t* args = (arg_t*)ece4750_malloc(arg_size);
    int* temp = (int*)ece4750_malloc(temp_size);

    if (!args || !temp) {
        // ece4750_wprintf(L"ERROR: Memory allocation failed.\n");
        ece4750_exit(1);
    }

    for (int i = 0; i < NUM_CORES; i++) {
        args[i].array = x;
        args[i].start = i * block_size;
        args[i].end = (i == NUM_CORES - 1) ? size : args[i].start + block_size;
    }

    for (int i = 1; i < NUM_CORES; i++) {
        ece4750_bthread_spawn(i, work, &args[i]);
    }
    work(&args[0]);

    for (int i = 1; i < NUM_CORES; i++) {
        ece4750_bthread_join(i);
    }

    merge(x, args[0].start, args[0].end, args[1].end, temp);
    merge(x, args[2].start, args[2].end, args[3].end, temp);
    merge(x, args[0].start, args[1].end, args[3].end, temp);

    ece4750_free(args);
    ece4750_free(temp);
}