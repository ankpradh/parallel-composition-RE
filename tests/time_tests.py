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
    if test.__name__ in ["test4", "test5"]:
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


# Tests for compositions of EM10, EM11, EM12 (Safety properties)
# Monolithic Composition with 3*4*3 = 36 states
# Serial and (both) Parallel Composition with 3+4+3 = 10 states

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


# Tests for compositions of EM13, EM14, EM15 (Co-safety properties)
# Monolithic Composition with 4*5*3 = 60 states
# Serial and (both) Parallel Composition with 4+5+3 = 12 states

def test5(Input):
    # Monolithic Test
    tsP = time.time()
    RCS, RCT, RCU = EM13(), EM14(), EM15()
    RC = monolithic_enforcer('RC', RCS, RCT, RCU)
    tsP = time.time()
    accept = RC.checkAccept(Input)
    teP = time.time()

    if (SIZEOF):
        print(asizeof.asized(RC, detail=1).format())

    # Serial Composition Test
    tsS = time.time()
    RCS, RCT, RCU = EM13("DFA"), EM14("DFA"), EM15("DFA")
    RC = serial_composition_enforcer(RCS, RCT, RCU)
    tsS = time.time()
    accept = RC.checkAccept(Input)
    teS = time.time()

    if (SIZEOF):
        print(asizeof.asized(RC, detail=1).format())

    # Maximal Prefix Parallel Composition Test
    tsM = time.time()
    RCS, RCT, RCU = EM13("pDFA"), EM14("pDFA"), EM15("pDFA")
    RC = maximal_prefix_parallel_enforcer(RCS, RCT, RCU)
    tsM = time.time()
    accept = RC.checkAccept(Input)
    teM = time.time()

    if (SIZEOF):
        print(asizeof.asized(RC, detail=1).format())

    # Parallel Composition Test
    tsC = time.time()
    RCS, RCT, RCU = EM13("pDFA"), EM14("pDFA"), EM15("pDFA")
    RC = parallel_enforcer(RCS, RCT, RCU)
    tsC = time.time()
    accept = RC.checkAccept(Input)
    teC = time.time()

    if (SIZEOF):
        print(asizeof.asized(RC, detail=1).format())

    return (teP - tsP)*1000, (teS - tsS)*1000, (teM - tsM)*1000, (teC - tsC)*1000

if __name__ == '__main__':
    Input1 = str(bin(15*1859))[2:]
    Input2 = "33322555556666661111444422"
    Input3 = "bbbbbbbbbbbbbbabbbbbbbbbbbbbb"
    avg_tests(1000, test1, Input1, 1)
    avg_tests(1000, test2, Input1, 2)
    avg_tests(1000, test3, Input2, 3)
    avg_tests(1000, test4, Input3, 4)
    avg_tests(1000, test5, Input3, 5)
    strings1 = generate_strings('01')
    strings2 = generate_strings('123456')
    strings3 = generate_strings('abc')
    for string in strings1:
        avg_tests(1000, test2, string, 2)
    for string in strings2:
        avg_tests(1000, test3, string, 3)
    for string in strings3:
        avg_tests(100, test4, string, 4)
        avg_tests(100, test5, string, 5)
    if (SIZEOF):
        print(EM_size)
