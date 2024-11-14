#!/bin/bash

# 定义实现和输入数据选项
impls=("base" "alt")
inputs=("loop1" "loop2" "loop3" "loop4" "loop5" "loop6")

# 循环遍历所有实现和输入组合
for impl in "${impls[@]}"; do
  for input in "${inputs[@]}"; do
    echo "Running: ../lab3_mem/mem-sim --impl $impl --input $input --stats"
    ../lab3_mem/mem-sim --impl $impl --input $input --stats
    echo "-------------------------------------------"
  done
done