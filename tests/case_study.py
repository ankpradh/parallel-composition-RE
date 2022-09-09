import sys
sys.path.append("..")

import time
import random
from pympler import asizeof
from src.enforcers import *

SIZEOF = False
EM_size = dict()

# Parallel Composition Runtime Enforcement: Case Study
# Simplistic Cruise Control scenario 
# Hexadecimal alphabet for 16 events

sigma_cc    = list('5')
sigma_ncc   = list('67AB')
sigma_e     = list('CDEF')
sigma_nccl  = list('7')
sigma_ncch  = list('AB')
sigma_AW    = list('6')
sigma_B_A   = list('89')
sigma_B_M   = list('23')
sigma_A     = list('1')
sigma_C     = list('4')
sigma_idle  = list('0')
sigma_1     = sigma_e + sigma_ncc + sigma_cc + sigma_B_A
sigma_2     = sigma_idle + sigma_C + sigma_A + sigma_B_M
sigma_B     = sigma_B_A + sigma_B_M
sigma       = sigma_2 + sigma_1


# Enforcers

def RE1e(Type="DFA"):
    """
    Events in sigma_cc must occur during cruise control
    """
    CC00, CC01, CC02, CC03 = state('CC00'), state('CC01'), state('CC02'), state('CC03')
    for i in sigma:
        CC03.transit[i] = CC03
    for i in sigma_cc:
        CC00.transit[i] = CC01
        CC01.transit[i] = CC01
        CC02.transit[i] = CC01
    for i in sigma_ncc:
        CC00.transit[i] = CC02
        CC01.transit[i] = CC02
        CC02.transit[i] = CC02
    for i in sigma_B_A:
        CC00.transit[i] = CC00
        CC01.transit[i] = CC02
        CC02.transit[i] = CC02
    for i in sigma_e:
        CC00.transit[i] = CC03
        CC01.transit[i] = CC03
        CC02.transit[i] = CC03
    for i in sigma_2:
        CC00.transit[i] = CC00
        CC01.transit[i] = CC01
        CC02.transit[i] = CC02
    if Type == "pDFA":
        CC0 = pDFA('CC0', sigma, [CC00, CC01, CC02, CC03], CC00, [CC01])
    else:
        CC0 = DFA('CC0', sigma, [CC00, CC01, CC02, CC03], CC00, [CC01])
    if (SIZEOF):
        EM_size["RE1e"] = asizeof.asizeof(CC0)
    return CC0


def RE2e(Type="DFA"):
    """
    If an event of sigma_AW occurs, then an event in sigma_B must 
    eventually occur, until which cruise control is disengaged
    """
    CC10, CC11 = state('CC10'), state('CC11')
    for i in sigma:
        CC10.transit[i] = CC10
        CC11.transit[i] = CC11
    for i in sigma_AW:
        CC10.transit[i] = CC11
    for i in sigma_B:
        CC11.transit[i] = CC10
    if Type == "pDFA":
        CC1 = pDFA('CC1', sigma, [CC10, CC11], CC10, [CC10])
    else:
        CC1 = DFA('CC1', sigma, [CC10, CC11], CC10, [CC10])
    if (SIZEOF):
        EM_size["RE2e"] = asizeof.asizeof(CC1)
    return CC1


def S1e(Type="DFA"):
    """
    Cruise control must be disengaged if a sequence contains an 
    element in sigma_A immediately followed by an element in 
    sigma_ncch and any element not in sigma_B
    """
    CC20, CC21, CC22, CC23 = state('CC20'), state('CC21'), state('CC22'), state('CC23')
    for i in sigma:
        CC20.transit[i] = CC20
        CC21.transit[i] = CC20
        CC22.transit[i] = CC23
        CC23.transit[i] = CC23
    for i in sigma_A:
        CC20.transit[i] = CC21
    for i in sigma_ncch:
        CC21.transit[i] = CC22
    for i in sigma_B:
        CC22.transit[i] = CC22
    if Type == "pDFA":
        CC2 = pDFA('CC2', sigma, [CC20, CC21, CC22, CC23], CC20, [CC20, CC21, CC22])
    else:
        CC2 = DFA('CC2', sigma, [CC20, CC21, CC22, CC23], CC20, [CC20, CC21, CC22])
    if (SIZEOF):
        EM_size["S1e"] = asizeof.asizeof(CC2)
    return CC2


def S2e(Type="DFA"):
    """
    Cruise Control must be disengaged if a sequence contains an 
    element in sigma_C immediately followed by an element in 
    sigma_nccl and any element not in sigma_B
    """
    CC30, CC31, CC32, CC33 = state('CC30'), state('CC31'), state('CC32'), state('CC33')
    for i in sigma:
        CC30.transit[i] = CC30
        CC31.transit[i] = CC30
        CC32.transit[i] = CC33
        CC33.transit[i] = CC33
    for i in sigma_C:
        CC30.transit[i] = CC31
    for i in sigma_nccl:
        CC31.transit[i] = CC32
    for i in sigma_B:
        CC32.transit[i] = CC32
    if Type == "pDFA":
        CC3 = pDFA('CC3', sigma, [CC30, CC31, CC32, CC33], CC30, [CC30, CC31, CC32])
    else:
        CC3 = DFA('CC3', sigma, [CC30, CC31, CC32, CC33], CC30, [CC30, CC31, CC32])
    if (SIZEOF):
        EM_size["S2e"] = asizeof.asizeof(CC3)
    return CC3


def CS1e(Type="DFA"):
    """
    Event in sigma_cc must occur at least once as a condition to
    engage in cruise control
    """
    CC40, CC41, CC42 = state('CC40'), state('CC41'), state('CC42')
    for i in sigma:
        CC41.transit[i] = CC41
        CC42.transit[i] = CC42
    for i in sigma_1:
        CC40.transit[i] = CC40
    for i in sigma_2:
        CC40.transit[i] = CC42
    for i in sigma_cc:
        CC40.transit[i] = CC41
    if Type == "pDFA":
        CC4 = pDFA('CC4', sigma, [CC40, CC41, CC42], CC40, [CC41])
    else:
        CC4 = DFA('CC4', sigma, [CC40, CC41, CC42], CC40, [CC41])
    if (SIZEOF):
        EM_size["CS1e"] = asizeof.asizeof(CC4)
    return CC4


def CS2e(Type="DFA"):
    """
    Event in sigma_cc subsequently followed by an element of
    sigma_A must occur at least once to engage in cruise control
    """
    CC50, CC51, CC52, CC53 = state('CC50'), state('CC51'), state('CC52'), state('CC53')
    for i in sigma:
        CC52.transit[i] = CC52
        CC53.transit[i] = CC53
    for i in sigma_1:
        CC50.transit[i] = CC50
    for i in sigma_2:
        CC50.transit[i] = CC53
        CC51.transit[i] = CC51
    for i in sigma_cc:
        CC50.transit[i] = CC51
        CC51.transit[i] = CC51
    for i in sigma_ncc:
        CC51.transit[i] = CC50
    for i in sigma_B_A:
        CC51.transit[i] = CC50
    for i in sigma_e:
        CC51.transit[i] = CC53
    for i in sigma_A:
        CC51.transit[i] = CC52
    if Type == "pDFA":
        CC5 = pDFA('CC5', sigma, [CC50, CC51, CC52, CC53], CC50, [CC52])
    else:
        CC5 = DFA('CC5', sigma, [CC50, CC51, CC52, CC53], CC50, [CC52])
    if (SIZEOF):
        EM_size["CS2e"] = asizeof.asizeof(CC5)
    return CC5


# For computing average runtimes 

def avg_tests(runs, test, string, test_name):
    test_avg_runs = runs
    test_Ptime = 0
    test_Ctime = 0
    for _ in range(test_avg_runs):
        _time = test(string)
        test_Ptime += _time[0]
        test_Ctime += _time[1]
    print("Test %s (%s)\n------------------- " %(test_name, len(string)))
    print("Computation time for Monolithic Enforcer (MCT): %f ms" %(test_Ptime/test_avg_runs))
    print("Computation time for Compositional Enforcer (PCT): %f ms" %(test_Ctime/test_avg_runs))
    print("Computation time for Compositional Enforcer (scaled down by # enforcers) (PCT/#E): %f ms" %(test_Ctime/(6*test_avg_runs)))
    print("Ratio R (PCT/#E/MCT) : %f ms\n" %((test_Ctime/(6*test_avg_runs))/(test_Ptime/test_avg_runs)))


# Generating random strings from given alphabet

def generate_strings(alphabet):
    strings = []
    # strings.append("".join(random.choices(alphabet, k=5000)))
    ranges = [(10**i, 5*10**i) for i in range(1, 6)]
    for size1, size2 in ranges:
        strings.append("".join(random.choices(alphabet, k=size1)))
        strings.append("".join(random.choices(alphabet, k=size2)))
    return strings


# Tests for compositions of RE1e, RE2e, S1e, S2e, CS1e and CS2e 
# Monolithic Composition with 4*2*4*4*3*4 = 1536 states
# Parallel Composition with 4+2+4+4+3+4 = 21 states

def test(Input):
    # Monolithic Test
    # tsP = time.time()
    RE1, RE2, S1, S2, CS1, CS2 = RE1e(), RE2e(), S1e(), S2e(), CS1e(), CS2e()
    CC = monolithic_enforcer('CC', RE1, RE2, S1, S2, CS1, CS2)
    # teP = time.time()
    tsP = time.time()
    accept = CC.checkAccept(Input)
    teP = time.time()

    if (SIZEOF):
        print(asizeof.asized(CC, detail=1).format())

    # Parallel Composition Test
    # tsC = time.time()
    RE1, RE2, S1, S2, CS1, CS2 = RE1e("pDFA"), RE2e("pDFA"), S1e("pDFA"), S2e("pDFA"), CS1e("pDFA"), CS2e("pDFA")
    CC = parallel_enforcer(RE1, RE2, S1, S2, CS1, CS2)
    # teC = time.time()
    tsC = time.time()
    accept = CC.checkAccept(Input)
    teC = time.time()

    if (SIZEOF):
        print(asizeof.asized(CC, detail=1).format())

    return (teP - tsP)*1000, (teC - tsC)*1000


if __name__ == '__main__':
    # Hexadecimal alphabet for 16 events
    strings = generate_strings(sigma)
    for string in strings:
        avg_tests(100, test, string, "Cruise Control")
    if (SIZEOF):
        print(EM_size)
