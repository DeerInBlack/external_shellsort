import os
import shutil
import heapq
import timeit
import functools
import numpy as np
from memory_profiler import memory_usage, profile


def shell_gap_seq(n):
    while (n := n // 2) > 0:
        yield n


def shell_sort(arr, gap_seq=None):
    n = len(arr)
    if gap_seq is None:
        gap_seq = shell_gap_seq(n)
    for gap in gap_seq:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp


def save_array_to_file(file_name, array_to_save):
    np.savetxt(file_name, array_to_save, fmt='%d')


def create_unsorted_file(n, file_path):
    arr = np.arange(n)
    np.random.shuffle(arr)
    save_array_to_file(file_path, arr)


def read_array(f, n):
    arr = []
    while len(arr) < n and (num := f.readline()):
        arr.append(int(num))
    return arr


@profile
def external_shell_sort(input_path, output_path, memory_amount, delete_tmp=True):
    with open(input_path, mode='r') as input_file:
        if os.path.exists('./tmp/'):
            shutil.rmtree('./tmp/')
        os.mkdir('./tmp/')
        tmp_f_count = 1
        while len(temp_arr := read_array(input_file, memory_amount)) > 0:
            shell_sort(temp_arr)
            save_array_to_file(f'./tmp/sorted_{tmp_f_count}', temp_arr)
            tmp_f_count += 1

    with open(output_path, 'w+') as output_file:
        min_heap = []
        for file_ind in range(1, tmp_f_count):
            if os.path.isfile(f'./tmp/sorted_{file_ind}'):
                file = open(f'./tmp/sorted_{file_ind}')
                if num := file.readline():
                    heapq.heappush(min_heap, (int(num), file))
        while len(min_heap) > 0:
            min_element, file = heapq.heappop(min_heap)
            output_file.write(f'{min_element}\n')
            if num := file.readline():
                heapq.heappush(min_heap, (int(num), file))
            else:
                file.close()
    if delete_tmp:
        shutil.rmtree('./tmp/')


def main():
    input_file = 'unsorted.txt'
    output_file = 'sorted.txt'
    n = 100000
    m = 10000
    create_unsorted_file(n, input_file)
    external_shell_sort(input_file, output_file, m)
    timer = timeit.Timer(functools.partial(external_shell_sort,
                                           input_file, output_file, m),
                         functools.partial(create_unsorted_file, n, input_file))
    elapsed_time = timer.timeit(1)
    memory_profile = memory_usage((external_shell_sort, (input_file, output_file, m)))
    memory_used = max(memory_profile)
    print(f'Input length: {n}; Processed length: {m}')
    print(f"Time: {elapsed_time} sec")
    print(f"Memory: {memory_used} MB")


if __name__ == "__main__":
    main()
