import time
import random
from pympler import asizeof
from enforcers import *
from maxMerge import *

SIZEOF = False
EM_size = dict()


# Enforcers

def EM1(Type="DFA"):
    A1, A2, A3 = state('A1'), state('A2'), state('A3')
    A1.transit['0'] = A1
    A1.transit['1'] = A2
    A2.transit['0'] = A3
    A2.transit['1'] = A1
    A3.transit['0'] = A2
    A3.transit['1'] = A3
    if Type == "pDFA":
        A = pDFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    else:
        A = DFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    if (SIZEOF):
        EM_size["EM1"] = asizeof.asizeof(A)
    return A

def EM2(Type="DFA"):
    B1, B2, B3, B4, B5 = state('B1'), state('B2'), state('B3'), state('B4'), state('B5')
    B1.transit['0'] = B1
    B1.transit['1'] = B2
    B2.transit['0'] = B3
    B2.transit['1'] = B4
    B3.transit['0'] = B5
    B3.transit['1'] = B1
    B4.transit['0'] = B2
    B4.transit['1'] = B3
    B5.transit['0'] = B4
    B5.transit['1'] = B5
    if Type == "pDFA":
        B = pDFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
    else:
        B = DFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1]) 
    if (SIZEOF):
        EM_size["EM2"] = asizeof.asizeof(B)
    return B

def EM3(Type="DFA"):
    C1, C2, C3, C4, C5, C6, C7 = state('C1'), state('C2'), state('C3'), state('C4'), state('C5'), state('C6'), state('C7')
    C1.transit['0'] = C1
    C1.transit['1'] = C2
    C2.transit['0'] = C3
    C2.transit['1'] = C4
    C3.transit['0'] = C5
    C3.transit['1'] = C6
    C4.transit['0'] = C7
    C4.transit['1'] = C1
    C5.transit['0'] = C2
    C5.transit['1'] = C3
    C6.transit['0'] = C4
    C6.transit['1'] = C5
    C7.transit['0'] = C6
    C7.transit['1'] = C7
    if Type == "pDFA":
        C = pDFA('C', ['0', '1'], [C1, C2, C3, C4, C5, C6, C7], C1, [C1])
    else:
        C = DFA('C', ['0', '1'], [C1, C2, C3, C4, C5, C6, C7], C1, [C1])
    if (SIZEOF):
        EM_size["EM3"] = asizeof.asizeof(C)
    return C    

def EM4(Type="DFA"):
    R11, R12 = state('R11'), state('R12')
    for i in range(1, 7):
        R11.transit[str(i)] = R11
        R12.transit[str(i)] = R12
    R11.transit['1'] = R12
    if Type == "pDFA":
        R1 = pDFA('R1', list('123456'), [R11, R12], R11, [R12])
    else:
        R1 = DFA('R1', list('123456'), [R11, R12], R11, [R12])
    if (SIZEOF):
        EM_size["EM4"] = asizeof.asizeof(R1)
    return R1

def EM5(Type="DFA"):
    R21, R22, R23 = state('R21'), state('R22'), state('R23')
    for i in range(1, 7):
        R21.transit[str(i)] = R21
        R22.transit[str(i)] = R22
        R23.transit[str(i)] = R23
    R21.transit['2'] = R22
    R22.transit['2'] = R23
    R23.transit['2'] = R22
    if Type == "pDFA":
        R2 = pDFA('R2', list('123456'), [R21, R22, R23], R21, [R23])
    else:
        R2 = DFA('R2', list('123456'), [R21, R22, R23], R21, [R23])
    if (SIZEOF):
        EM_size["EM5"] = asizeof.asizeof(R2)
    return R2

def EM6(Type="DFA"):
    R31, R32, R33, R34 = state('R31'), state('R32'), state('R33'), state('R34')
    for i in range(1, 7):
        R31.transit[str(i)] = R31
        R32.transit[str(i)] = R32
        R33.transit[str(i)] = R33
        R34.transit[str(i)] = R34
    R31.transit['3'] = R32
    R32.transit['3'] = R33
    R33.transit['3'] = R34
    R34.transit['3'] = R32
    if Type == "pDFA":
        R3 = pDFA('R3', list('123456'), [R31, R32, R33, R34], R31, [R34])
    else:
        R3 = DFA('R3', list('123456'), [R31, R32, R33, R34], R31, [R34])
    if (SIZEOF):
        EM_size["EM6"] = asizeof.asizeof(R3)
    return R3

def EM7(Type="DFA"):
    R41, R42, R43, R44, R45 = state('R41'), state('R42'), state('R43'), state('R44'), state('R45')
    for i in range(1, 7):
        R41.transit[str(i)] = R41
        R42.transit[str(i)] = R42
        R43.transit[str(i)] = R43
        R44.transit[str(i)] = R44
        R45.transit[str(i)] = R45
    R41.transit['4'] = R42
    R42.transit['4'] = R43
    R43.transit['4'] = R44
    R44.transit['4'] = R45
    R45.transit['4'] = R42
    if Type == "pDFA":
        R4 = pDFA('R4', list('123456'), [R41, R42, R43, R44, R45], R41, [R45])
    else:
        R4 = DFA('R4', list('123456'), [R41, R42, R43, R44, R45], R41, [R45])
    if (SIZEOF):
        EM_size["EM7"] = asizeof.asizeof(R4)
    return R4

def EM8(Type="DFA"):
    R51, R52, R53, R54, R55, R56 = state('R51'), state('R52'), state('R53'), state('R54'), state('R55'), state('R56')
    for i in range(1, 7):
        R51.transit[str(i)] = R51
        R52.transit[str(i)] = R52
        R53.transit[str(i)] = R53
        R54.transit[str(i)] = R54
        R55.transit[str(i)] = R55
        R56.transit[str(i)] = R56
    R51.transit['5'] = R52
    R52.transit['5'] = R53
    R53.transit['5'] = R54
    R54.transit['5'] = R55
    R55.transit['5'] = R56
    R56.transit['5'] = R52
    if Type == "pDFA":
        R5 = pDFA('R5', list('123456'), [R51, R52, R53, R54, R55, R56], R51, [R56])
    else:
        R5 = DFA('R5', list('123456'), [R51, R52, R53, R54, R55, R56], R51, [R56])
    if (SIZEOF):
        EM_size["EM8"] = asizeof.asizeof(R5)
    return R5

def EM9(Type="DFA"):
    R61, R62, R63, R64, R65, R66, R67 = state('R61'), state('R62'), state('R63'), state('R64'), state('R65'), state('R66'), state('R67')
    for i in range(1, 7):
        R61.transit[str(i)] = R61
        R62.transit[str(i)] = R62
        R63.transit[str(i)] = R63
        R64.transit[str(i)] = R64
        R65.transit[str(i)] = R65
        R66.transit[str(i)] = R66
        R67.transit[str(i)] = R67
    R61.transit['6'] = R62
    R62.transit['6'] = R63
    R63.transit['6'] = R64
    R64.transit['6'] = R65
    R65.transit['6'] = R66
    R66.transit['6'] = R67
    R67.transit['6'] = R62
    if Type == "pDFA":
        R6 = pDFA('R6', list('123456'), [R61, R62, R63, R64, R65, R66, R67], R61, [R67])
    else:
        R6 = DFA('R6', list('123456'), [R61, R62, R63, R64, R65, R66, R67], R61, [R67])
    if (SIZEOF):
        EM_size["EM9"] = asizeof.asizeof(R6)
    return R6


# For computing average runtimes 

def avg_tests(runs, test, string, test_num):
    test_avg_runs = runs
    test_Ptime = 0
    test_Ctime = 0
    for _ in range(test_avg_runs):
        _time = test(string)
        test_Ptime += _time[0]
        test_Ctime += _time[1]
    print("Test %s\n------" %(test_num))
    print("Computation time for Monolithic Enforcer : %f ms" %(test_Ptime/test_avg_runs))
    print("Computation time for Compositional Enforcer : %f ms\n" %(test_Ctime/test_avg_runs))


# Generating random strings from given alphabet

def generate_strings(alphabet):
    strings = []
    ranges = [(10**i, 5*10**i) for i in range(1, 6)]
    for size1, size2 in ranges:
        strings.append("".join(random.choices(alphabet, k=size1)))
        strings.append("".join(random.choices(alphabet, k=size2)))
    return strings


# Tests for compositions of EM1 and EM2 with 3*5 = 15 states

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


# Tests for compositions of EM1, EM2 and EM3 with 3*5*7 = 105 states

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


# Tests for compositions of EM4, EM5, EM6, EM7, EM8 and EM9 with 2*3*4*5*6 = 720 states

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

if __name__ == '__main__':
    Input1 = str(bin(15*1859))[2:]
    Input2 = "33322555556666661111444422"
    avg_tests(1000, test1, Input1, 1)
    avg_tests(1000, test2, Input1, 2)
    avg_tests(1000, test3, Input2, 3)
    strings1 = generate_strings('01')
    strings2 = generate_strings('123456')
    for string in strings1:
        avg_tests(1000, test2, string, 2)
    for string in strings2:
        avg_tests(1000, test3, string, 3)
    if (SIZEOF):
        print(EM_size)
