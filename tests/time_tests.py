import sys
import time
import random
sys.path.append("..")

from pympler import asizeof
from test_automata import *

# For computing average runtimes 

def avg_tests(runs, test, string, test_num):
    test_avg_runs = runs
    test_Ptime = 0
    test_Ctime = 0
    if test.__name__ == "test4":
        test_Stime = 0
        test_Mtime = 0
        for _ in range(test_avg_runs):
            _time = test(string)
            test_Ptime += _time[0]
            test_Stime += _time[1]
            test_Mtime += _time[2]
            test_Ctime += _time[3]
        print("Test %s (%s)\n------------------- " %(test_num, len(string)))
        print("Computation time for Monolithic Enforcer : %f ms" %(test_Ptime/test_avg_runs))
        print("Computation time for Serial Composition : %f ms" %(test_Stime/test_avg_runs))
        print("Computation time for Maximal Prefix Parallel Composition : %f ms" %(test_Mtime/test_avg_runs))
        print("Computation time for Parallel Composition : %f ms\n" %(test_Ctime/test_avg_runs))
    else:
        for _ in range(test_avg_runs):
            _time = test(string)
            test_Ptime += _time[0]
            test_Ctime += _time[1]
        print("Test %s (%s)\n------------------- " %(test_num, len(string)))
        print("Computation time for Monolithic Enforcer : %f ms" %(test_Ptime/test_avg_runs))
        print("Computation time for Parallel Composition : %f ms\n" %(test_Ctime/test_avg_runs))


# Generating random strings from given alphabet

def generate_strings(alphabet):
    strings = []
    ranges = [(10**i, 5*10**i) for i in range(1, 6)]
    for size1, size2 in ranges:
        strings.append("".join(random.choices(alphabet, k=size1)))
        strings.append("".join(random.choices(alphabet, k=size2)))
    return strings


# Tests for compositions of EM1 and EM2 
# Monolithic Composition with 3*5 = 15 states
# Parallel Composition with 3+5 = 8 states

def test1(Input):
    # Monolithic Test
    tsP = time.time()
    A, B = EM1(), EM2()
    A_B = monolithic_enforcer('A_B', A, B)
    tsP = time.time()
    accept = A_B.checkAccept(Input)
    teP = time.time()
    
    # Parallel Composition Test
    tsC = time.time()
    A, B = EM1("pDFA"), EM2("pDFA")
    A_B = parallel_enforcer(A, B)
    tsC = time.time()
    accept = A_B.checkAccept(Input)
    teC = time.time()
    
    return (teP - tsP)*1000, (teC - tsC)*1000


# Tests for compositions of EM1, EM2 and EM3 
# Monolithic Composition with 3*5*7 = 105 states
# Parallel Composition with 3+5+7 = 15 states

def test2(Input):
    # Monolithic Test
    tsP = time.time()
    A, B, C = EM1(), EM2(), EM3()
    A_B_C = monolithic_enforcer('A_B_C', A, B, C)
    tsP = time.time()
    accept = A_B_C.checkAccept(Input)
    teP = time.time()

    if (SIZEOF):
        print(asizeof.asized(A_B_C, detail=1).format())

    # Parallel Composition Test
    tsC = time.time()
    A, B, C = EM1("pDFA"), EM2("pDFA"), EM3("pDFA")
    A_B_C = parallel_enforcer(A, B, C)
    tsC = time.time()
    accept = A_B_C.checkAccept(Input)
    teC = time.time()

    return (teP - tsP)*1000, (teC - tsC)*1000


# Tests for compositions of EM4, EM5, EM6, EM7, EM8 and EM9
# Monolithic Composition with 2*3*4*5*6*7 = 5040 states
# Parallel Composition with 2+3+4+5+6+7 = 27 states

def test3(Input):
    # Monolithic Test
    tsP = time.time()
    R1, R2, R3, R4, R5, R6 = EM4(), EM5(), EM6(), EM7(), EM8(), EM9()
    R = monolithic_enforcer('R', R1, R2, R3, R4, R5, R6)
    tsP = time.time()
    accept = R.checkAccept(Input)
    teP = time.time()

    if (SIZEOF):
        print(asizeof.asized(R, detail=1).format())

    # Parallel Composition Test
    tsC = time.time()
    R1, R2, R3, R4, R5, R6 = EM4("pDFA"), EM5("pDFA"), EM6("pDFA"), EM7("pDFA"), EM8("pDFA"), EM9("pDFA")
    R = parallel_enforcer(R1, R2, R3, R4, R5, R6)
    tsC = time.time()
    accept = R.checkAccept(Input)
    teC = time.time()

    return (teP - tsP)*1000, (teC - tsC)*1000

def test4(Input):
    # Monolithic Test
    tsP = time.time()
    RS, RT, RU = EM10(), EM11(), EM12()
    R = monolithic_enforcer('R', RS, RT, RU)
    tsP = time.time()
    accept = R.checkAccept(Input)
    teP = time.time()

    if (SIZEOF):
        print(asizeof.asized(R, detail=1).format())

    # Serial Composition Test
    tsS = time.time()
    RS, RT, RU = EM10("DFA"), EM11("DFA"), EM12("DFA")
    R = serial_composition_enforcer(RS, RT, RU)
    tsS = time.time()
    accept = R.checkAccept(Input)
    teS = time.time()

    if (SIZEOF):
        print(asizeof.asized(R, detail=1).format())

    # Maximal Prefix Parallel Composition Test
    tsM = time.time()
    RS, RT, RU = EM10("pDFA"), EM11("pDFA"), EM12("pDFA")
    R = maximal_prefix_parallel_enforcer(RS, RT, RU)
    tsM = time.time()
    accept = R.checkAccept(Input)
    teM = time.time()

    if (SIZEOF):
        print(asizeof.asized(R, detail=1).format())

    # Parallel Composition Test
    tsC = time.time()
    RS, RT, RU = EM10("pDFA"), EM11("pDFA"), EM12("pDFA")
    R = parallel_enforcer(RS, RT, RU)
    tsC = time.time()
    accept = R.checkAccept(Input)
    teC = time.time()

    if (SIZEOF):
        print(asizeof.asized(R, detail=1).format())

    return (teP - tsP)*1000, (teS - tsS)*1000, (teM - tsM)*1000, (teC - tsC)*1000

if __name__ == '__main__':
    Input1 = str(bin(15*1859))[2:]
    Input2 = "33322555556666661111444422"
    avg_tests(1000, test1, Input1, 1)
    avg_tests(1000, test2, Input1, 2)
    avg_tests(1000, test3, Input2, 3)
    strings1 = generate_strings('01')
    strings2 = generate_strings('123456')
    strings3 = generate_strings('abc')
    for string in strings1:
        avg_tests(1000, test2, string, 2)
    for string in strings2:
        avg_tests(1000, test3, string, 3)
    for string in strings3:
        avg_tests(100, test4, string, 4)
    if (SIZEOF):
        print(EM_size)
