import sys
sys.path.append("..")

from pympler import asizeof
from src.enforcers import *

SIZEOF = False
EM_size = dict()

# Enforcers
# Alphabet for EM1, EM2 and EM3 = {0, 1}

def EM1(Type="DFA"):
    """
    Accepting binary strings divisible by 3
    """
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
    """
    Accepting binary strings divisible by 5
    """
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
    """
    Accepting binary strings divisible by 7
    """
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


# Alphabet for EM4, EM5, EM6, EM7, EM8 and EM9 = {1, 2, 3, 4, 5, 6}

def EM4(Type="DFA"):
    """
    Accepting strings with atleast one '1'
    """
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
    """
    Accepting strings with '2' repeated in multiples of 2
    """
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
    """
    Accepting strings with '3' repeated in multiples of 3
    """
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
    """
    Accepting strings with '4' repeated in multiples of 4
    """
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
    """
    Accepting strings with '5' repeated in multiples of 5
    """
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
    """
    Accepting strings with '6' repeated in multiples of 6
    """
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

# Alphabet for EM10, EM11, EM12 = {a, b, c}

def EM10(Type="DFA"):
    """
    After 'b' occurs, it is forbidden to have 'a'
    """
    RS1, RS2, RS3 = state('RS1'), state('RS2'), state('RS3')
    RS1.transit['a'] = RS1
    RS1.transit['b'] = RS2
    RS1.transit['c'] = RS1
    RS2.transit['a'] = RS3
    RS2.transit['b'] = RS2
    RS2.transit['c'] = RS2
    RS3.transit['a'] = RS3
    RS3.transit['b'] = RS3
    RS3.transit['c'] = RS3
    if Type == "pDFA":
        RS = pDFA('RS', list('abc'), [RS1, RS2, RS3], RS1, [RS1, RS2])
    else:
        RS = DFA('RS', list('abc'), [RS1, RS2, RS3], RS1, [RS1, RS2])
    if (SIZEOF):
        EM_size["EM10"] = asizeof.asizeof(RS)
    return RS

def EM11(Type="DFA"):
    """
    At most two 'a' actions occur
    """
    RT1, RT2, RT3, RT4 = state('RT1'), state('RT2'), state('RT3'), state('RT4')
    RT1.transit['a'] = RT2
    RT1.transit['b'] = RT1
    RT1.transit['c'] = RT1
    RT2.transit['a'] = RT3
    RT2.transit['b'] = RT2
    RT2.transit['c'] = RT2
    RT3.transit['a'] = RT4
    RT3.transit['b'] = RT3
    RT3.transit['c'] = RT3
    RT4.transit['a'] = RT4
    RT4.transit['b'] = RT4
    RT4.transit['c'] = RT4
    if Type == "pDFA":
        RT = pDFA('RT', list('abc'), [RT1, RT2, RT3, RT4], RT1, [RT1, RT2, RT3])
    else:
        RT = DFA('RT', list('abc'), [RT1, RT2, RT3, RT4], RT1, [RT1, RT2, RT3])
    if (SIZEOF):
        EM_size["EM11"] = asizeof.asizeof(RT)
    return RT

def EM12(Type="DFA"):
    """
    There are no two consecutive 'a' actions
    """
    RU1, RU2, RU3 = state('RU1'), state('RU2'), state('RU3')
    RU1.transit['a'] = RU2
    RU1.transit['b'] = RU1
    RU1.transit['c'] = RU1
    RU2.transit['a'] = RU3
    RU2.transit['b'] = RU1
    RU2.transit['c'] = RU1
    RU3.transit['a'] = RU3
    RU3.transit['b'] = RU3
    RU3.transit['c'] = RU3
    if Type == "pDFA":
        RU = pDFA('RU', list('abc'), [RU1, RU2, RU3], RU1, [RU1, RU2])
    else:
        RU = DFA('RU', list('abc'), [RU1, RU2, RU3], RU1, [RU1, RU2])
    if (SIZEOF):
        EM_size["EM12"] = asizeof.asizeof(RU)
    return RU

def EM13(Type="DFA"):
    """
    The first two actions should be 'a' followed by 'b'
    """
    RCS1, RCS2, RCS3, RCS4 = state('RCS1'), state('RCS2'), state('RCS3'), state('RCS4')
    RCS1.transit['a'] = RCS2
    RCS1.transit['b'] = RCS4
    RCS1.transit['c'] = RCS4
    RCS2.transit['a'] = RCS4
    RCS2.transit['b'] = RCS3
    RCS2.transit['c'] = RCS4
    RCS3.transit['a'] = RCS3
    RCS3.transit['b'] = RCS3
    RCS3.transit['c'] = RCS3
    RCS4.transit['a'] = RCS4
    RCS4.transit['b'] = RCS4
    RCS4.transit['c'] = RCS4
    if Type == "pDFA":
        RCS = pDFA('RCS', list('abc'), [RCS1, RCS2, RCS3, RCS4], RCS1, [RCS3])
    else:
        RCS = DFA('RCS', list('abc'), [RCS1, RCS2, RCS3, RCS4], RCS1, [RCS3])
    if (SIZEOF):
        EM_size["EM13"] = asizeof.asizeof(RCS)
    return RCS

def EM14(Type="DFA"):
    """
    The first three actions should be 'a' followed by 'b' followed by 'c'
    """
    RCT1, RCT2, RCT3, RCT4, RCT5 = state('RCT1'), state('RCT2'), state('RCT3'), state('RCT4'), state('RCT5')
    RCT1.transit['a'] = RCT2
    RCT1.transit['b'] = RCT5
    RCT1.transit['c'] = RCT5
    RCT2.transit['a'] = RCT5
    RCT2.transit['b'] = RCT3
    RCT2.transit['c'] = RCT5
    RCT3.transit['a'] = RCT5
    RCT3.transit['b'] = RCT5
    RCT3.transit['c'] = RCT4
    RCT4.transit['a'] = RCT4
    RCT4.transit['b'] = RCT4
    RCT4.transit['c'] = RCT4
    RCT5.transit['a'] = RCT5
    RCT5.transit['b'] = RCT5
    RCT5.transit['c'] = RCT5
    if Type == "pDFA":
        RCT = pDFA('RCT', list('abc'), [RCT1, RCT2, RCT3, RCT4, RCT5], RCT1, [RCT4])
    else:
        RCT = DFA('RCT', list('abc'), [RCT1, RCT2, RCT3, RCT4, RCT5], RCT1, [RCT4])
    if (SIZEOF):
        EM_size["EM14"] = asizeof.asizeof(RCT)
    return RCT

def EM15(Type="DFA"):
    """
    Event 'a' followed by event 'b' must occur at least once
    """
    RCU1, RCU2, RCU3 = state('RCU1'), state('RCU2'), state('RCU3')
    RCU1.transit['a'] = RCU2
    RCU1.transit['b'] = RCU1
    RCU1.transit['c'] = RCU1
    RCU2.transit['a'] = RCU1
    RCU2.transit['b'] = RCU3
    RCU2.transit['c'] = RCU1
    RCU3.transit['a'] = RCU3
    RCU3.transit['b'] = RCU3
    RCU3.transit['c'] = RCU3
    if Type == "pDFA":
        RCU = pDFA('RCU', list('abc'), [RCU1, RCU2, RCU3], RCU1, [RCU3])
    else:
        RCU = DFA('RCU', list('abc'), [RCU1, RCU2, RCU3], RCU1, [RCU3])
    if (SIZEOF):
        EM_size["EM15"] = asizeof.asizeof(RCU)
    return RCU
