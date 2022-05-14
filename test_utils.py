


import time


max_items = 20


def run_test(method, args, expected):
    start_time = time.time()
    result = method(*args)
    duration = time.time() - start_time
    success = result == expected
    printable_args = [(a[:max_items] if type(a) is list or type(a) is tuple else a) for a in args]
    printable_result = result[:max_items] if type(result) is list or type(result) is tuple else result
    printable_expected = expected[:max_items] if type(expected) is list or type(expected) is tuple else expected
    print('{} in {:.3f} sec, args: {} result: {} expected: {}'.format(
        '\x1b[1;32;40m[PASS]\x1b[0m' if success else '\x1b[1;31;40m[FAIL]\x1b[0m',
        duration,
        printable_args,
        printable_result, printable_expected))
 