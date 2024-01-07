def solution(A, B):
    rotations = 0
    solution = False

    while not solution and rotations <= len(B):
        print(B)
        solution = True
        for i in range(len(B)):
            if B[i] == A[i]:
                solution = False
                break
        if not solution:
            B = B[-1:] + B[:-1]
            rotations += 1

    return rotations if solution else -1

from test_utils import run_test

method = solution

run_test(method, ([1, 3, 5, 2, 8, 7], [7, 1, 9, 8, 5, 7]), 2)
run_test(method, ([1, 1, 1, 1], [1, 2, 3, 4]), -1)
run_test(method, ([3, 5, 0, 2, 4], [1, 3, 10, 6, 7]), 0)
