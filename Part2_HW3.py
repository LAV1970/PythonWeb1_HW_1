import multiprocessing
import time


def factorize_parallel(num):
    factors = [i for i in range(1, num + 1) if num % i == 0]
    return factors


def factorize(*numbers):
    result = []
    for num in numbers:
        # If a single number is provided, delegate to factorize_parallel
        if isinstance(num, int):
            factors = factorize_parallel(num)
        else:
            factors = [i for i in range(1, num + 1) if num % i == 0]
        result.append(factors)
    return result


def measure_time():
    numbers_to_factorize = [12, 8, 15]

    start_time = time.time()
    result_factors = factorize(*numbers_to_factorize)
    end_time = time.time()

    for num, factors in zip(numbers_to_factorize, result_factors):
        print(f"Factors of {num}: {factors}")

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")


a, b, c, d = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [
    1,
    2,
    4,
    5,
    7,
    10,
    14,
    20,
    28,
    35,
    70,
    140,
    76079,
    152158,
    304316,
    380395,
    532553,
    760790,
    1065106,
    1521580,
    2130212,
    2662765,
    5325530,
    10651060,
]

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    print(f"Number of CPU cores: {num_cores}")
    measure_time()
