from automata import state
from enforcer import pDFA

def maxMerge(_input, *D):
    """ Function to maximally merge the contents of external buffers of a set of 2 or more parallel enforcers.
    Args
    ----
    _input : String of input characters belonging to the alphabet.
    *D     : set of Enforcer automaton (should be atleast 2 lest AssertionError occurs.

    Returns
    -------
    List of strings of characters satisfying the combined property enforced by the composition of all enforcers.
    
    Testable Code
    -------------
    >>> t = str(bin(15*1859))[2:]
    >>> print(len(t), int(t, 2))
    15 27885
    >>> A1, A2, A3 = state('A1'), state('A2'), state('A3')
    >>> B1, B2, B3, B4, B5 = state('B1'), state('B2'), state('B3'), state('B4'), state('B5')
    >>> A1.transit['0'] = A1
    >>> A1.transit['1'] = A2
    >>> A2.transit['0'] = A3
    >>> A2.transit['1'] = A1
    >>> A3.transit['0'] = A2
    >>> A3.transit['1'] = A3
    >>> B1.transit['0'] = B1
    >>> B1.transit['1'] = B2
    >>> B2.transit['0'] = B3
    >>> B2.transit['1'] = B4
    >>> B3.transit['0'] = B5
    >>> B3.transit['1'] = B1
    >>> B4.transit['0'] = B2
    >>> B4.transit['1'] = B3
    >>> B5.transit['0'] = B4
    >>> B5.transit['1'] = B5
    >>> A = pDFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    >>> B = pDFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
    >>> maxMerge(t, A, B)
    ['110110011', '101101']
    """
    assert len(D) > 1, "Too few enforcers to merge"
    output = []
    out_buffer_len = [automata.lenOut() for automata in D]
    for i in _input:
        signal = [0 for automata in D]
        for idx, automata in enumerate(D):
            automata.runInput(i)
            curr_size = automata.lenOut()
            if curr_size != out_buffer_len[idx] and curr_size != 0:
                out_buffer_len[idx] = curr_size
                signal[idx] = 1
        if all(signal) == True:
            enforced = D[0].outBuffer()
            for automata in D:
                automata.flushOutBuffer()
            output.append(''.join(enforced))
    return output

if __name__ == '__main__':
    debug = True
    import doctest
    doctest.testmod()
