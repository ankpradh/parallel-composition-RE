import time
from pympler import asizeof
from buffer_merge import *

SIZEOF = False
EM_size = dict()

def EM1():
    A1, A2, A3 = state('A1'), state('A2'), state('A3')
    A1.transit['0'] = A1
    A1.transit['1'] = A2
    A2.transit['0'] = A3
    A2.transit['1'] = A1
    A3.transit['0'] = A2
    A3.transit['1'] = A3
    A = eDFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    if (SIZEOF):
        EM_size["EM1"] = asizeof.asizeof(A)
    return A

def EM2():
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
    B = eDFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
    if (SIZEOF):
        EM_size["EM2"] = asizeof.asizeof(B)
    return B

def EM3():
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
    C = eDFA('C', ['0', '1'], [C1, C2, C3, C4, C5, C6, C7], C1, [C1])
    if (SIZEOF):
        EM_size["EM3"] = asizeof.asizeof(C)
    return C    

def EM4():
    R11, R12 = state('R11'), state('R12')
    for i in range(1, 7):
        R11.transit[str(i)] = R11
        R12.transit[str(i)] = R12
    R11.transit['1'] = R12
    R1 = eDFA('R1', list('123456'), [R11, R12], R11, [R12])
    if (SIZEOF):
        EM_size["EM4"] = asizeof.asizeof(R1)
    return R1

def EM5():
    R21, R22, R23 = state('R21'), state('R22'), state('R23')
    for i in range(1, 7):
        R21.transit[str(i)] = R21
        R22.transit[str(i)] = R22
        R23.transit[str(i)] = R23
    R21.transit['2'] = R22
    R22.transit['2'] = R23
    R23.transit['2'] = R22
    R2 = eDFA('R2', list('123456'), [R21, R22, R23], R21, [R23])
    if (SIZEOF):
        EM_size["EM5"] = asizeof.asizeof(R2)
    return R2

def EM6():
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
    R3 = eDFA('R3', list('123456'), [R31, R32, R33, R34], R31, [R34])
    if (SIZEOF):
        EM_size["EM6"] = asizeof.asizeof(R3)
    return R3

def EM7():
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
    R4 = eDFA('R4', list('123456'), [R41, R42, R43, R44, R45], R41, [R45])
    if (SIZEOF):
        EM_size["EM7"] = asizeof.asizeof(R4)
    return R4

def EM8():
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
    R5 = eDFA('R5', list('123456'), [R51, R52, R53, R54, R55, R56], R51, [R56])
    if (SIZEOF):
        EM_size["EM8"] = asizeof.asizeof(R5)
    return R5

def EM9():
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
    R6 = eDFA('R6', list('123456'), [R61, R62, R63, R64, R65, R66, R67], R61, [R67])
    if (SIZEOF):
        EM_size["EM9"] = asizeof.asizeof(R6)
    return R6

def test1():
    A, B = EM1(), EM2()
    Input = str(bin(15*1859))[2:]
    tsP = time.time()
    A_B = product(A, B, 'A_B')
    accept = A_B.checkAccept(Input)
    teP = time.time()
    tsC = time.time()
    accept = maxMerge(Input, A, B)
    teC = time.time()
    return (teP - tsP)*1000, (teC - tsC)*1000

def avg_test1(runs):
    test1_avg_runs = runs
    test1_Ptime = 0
    test1_Ctime = 0
    for _ in range(test1_avg_runs):
        _time = test1()
        test1_Ptime += _time[0]
        test1_Ctime += _time[1]
    print("Test 1\n------")
    print("Computation time for Monolithic Enforcer : %f ms" %(test1_Ptime/test1_avg_runs))
    print("Computation time for Compositional Enforcer : %f ms\n" %(test1_Ctime/test1_avg_runs))

def test2():
    A, B, C = EM1(), EM2(), EM3()
    Input = str(bin(105*1859))[2:]
    tsP = time.time()
    A_B = product(A, B, 'A_B')
    A_B_C = product(A_B, C, 'A_B_C')
    if (SIZEOF):
        print(asizeof.asized(A_B_C, detail=1).format())
    accept = A_B_C.checkAccept(Input)
    teP = time.time()
    tsC = time.time()
    accept = maxMerge(Input, A, B, C)
    teC = time.time()
    return (teP - tsP)*1000, (teC - tsC)*1000

def avg_test2(runs):
    test2_avg_runs = runs
    test2_Ptime = 0
    test2_Ctime = 0
    for _ in range(test2_avg_runs):
        _time = test2()
        test2_Ptime += _time[0]
        test2_Ctime += _time[1]
    print("Test 2\n------")
    print("Computation time for Monolithic Enforcer : %f ms" %(test2_Ptime/test2_avg_runs))
    print("Computation time for Compositional Enforcer : %f ms\n" %(test2_Ctime/test2_avg_runs))

def test3():
    R1, R2, R3, R4, R5, R6 = EM4(), EM5(), EM6(), EM7(), EM8(), EM9()
    Input = "33322555556666661111444422"
    tsP = time.time()
    R = product(R1, R2, 'R1_R2')
    R = product(R, R3, 'R1_R2_R3')
    R = product(R, R4, 'R1_R2_R3_R4')
    R = product(R, R5, 'R1_R2_R3_R4_R5')
    R = product(R, R6, 'R1_R2_R3_R4_R5_R6')
    if (SIZEOF):
        print(asizeof.asized(R, detail=1).format())
    accept = R.checkAccept(Input)
    teP = time.time()
    tsC = time.time()
    accept = maxMerge(Input, R1, R2, R3, R4, R5, R6)
    teC = time.time()
    return (teP - tsP)*1000, (teC - tsC)*1000

def avg_test3(runs):
    test3_avg_runs = runs
    test3_Ptime = 0
    test3_Ctime = 0
    for _ in range(test3_avg_runs):
        _time = test3()
        test3_Ptime += _time[0]
        test3_Ctime += _time[1]
    print("Test 3\n------")
    print("Computation time for Monolithic Enforcer : %f ms" %(test3_Ptime/test3_avg_runs))
    print("Computation time for Compositional Enforcer : %f ms\n" %(test3_Ctime/test3_avg_runs))

if __name__ == '__main__':
    avg_test1(1000)
    avg_test2(1000)
    avg_test3(1000)
    if (SIZEOF):
        print(EM_size)
