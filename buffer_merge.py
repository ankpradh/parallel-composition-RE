INBUFFER = 10

class state(object):
    """ Defines a basic state with a dictionary of transitions from that state. """
    def __init__(self, name):
        self.name = name
        self.transit = dict()

class eDFA(object):
    """ Class for enforcing a single property.
        
    Testable Code
    -------------
    >>> a = state('a')
    >>> b = state('b')
    >>> a.transit['0'] = b
    >>> b.transit['0'] = a
    >>> b.transit['1'] = b
    >>> a.transit['1'] = a
    >>> D = eDFA('D', ['0', '1'], [a, b], a, [a])
    >>> input1 = '001010010'
    >>> D.checkAccept(input1)
    ['00', '1', '010', '010']
    >>> D.outBuffer()
    ['0', '0', '1', '0', '1', '0', '0', '1', '0']
    >>> D.inBuffer()
    []
    >>> input2 = '000'
    >>> D.checkAccept(input2)
    ['00']
    >>> D.outBuffer()
    ['0', '0', '1', '0', '1', '0', '0', '1', '0', '0', '0']
    >>> D.inBuffer()
    ['0']
    >>> input3 = '010011'
    >>> D.checkAccept(input3)
    ['0', '1', '00', '1', '1']
    >>> D.outBuffer()
    ['0', '0', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '1', '1']
    >>> D.inBuffer()
    []
    """
    def __init__(self, name, alphabet, states=None, start=None, end=None):
        """ Initializes necessary variables and buffers to facilitate ease of use at runtime. """
        self.name = name
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.end = end
        self.curr_state = self.start
        self.buffer = []
        self.out_buffer = []
        self.out_len = 0

    def runInput(self, _input):
        """ Runs the given input instance through the automata starting at the current state updated from the previous input. """
        self.buffer.append(_input)
        self.curr_state = self.curr_state.transit[_input]
        var = self.curr_state
        if var in self.end:
            self.out_buffer += self.buffer # Add to External Buffer
            self.out_len += len(self.buffer)
            self.buffer = [] # Flush Internal Buffer
        return var

    def checkAccept(self, _input):
        """ Checks whether the input in accepted by the automaton. """
        index = []
        output = []
        for idx, i in enumerate(_input):
            State = self.runInput(i)
            if State in self.end:
                index.append(idx)
        if index:
            output.append(_input[: index[0] + 1])
            for i in range(len(index) - 1):
                output.append(_input[index[i] + 1 : index[i + 1] + 1])
        return output

    def flushOutBuffer(self):
    	""" Flushes the contents of the external buffer. """
        self.out_buffer = []
        self.out_len = 0

    def lenOut(self):
    	""" Returns the size of the external buffer. """
        return self.out_len

    def outBuffer(self):
        """ Returns the contents of the external buffer. """
        return self.out_buffer

    def inBuffer(self):
        """ Returns the contents of the internal buffer. """
        return self.buffer


def maxMerge(_input, *D):
    """ Function to maximally merge the contents of external buffers of a set of 2 or more enforcers.
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
    >>> A = eDFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    >>> B = eDFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
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

def product(A, B, p_name):
    """ Computes the product automaton of two eDFAs.

    Args
    ----
    A, B    : variables referencing an eDFA.
    p_name  : name of the product automaton.

    Returns
    -------
    An eDFA which is a product automaton of input eDFA A and B with name "p_name".
    
    Testable Code
    -------------
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
    >>> A = eDFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    >>> B = eDFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
    >>> print(A.start.transit['1'].name, B.start.name)
    A2 B1
    >>> C = product(A, B, 'C')
    >>> C.alphabet
    ['0', '1']
    >>> C.start.name
    'A1_B1'
    >>> for s in C.end:
    ...     print(s.name)
    A1_B1
    >>> Input = str(bin(15*1859))[2:]
    >>> C.checkAccept(Input)
    ['110110011', '101101']
    """
    class state(object):
        def __init__(self, name):
            self.name = name
            self.transit = dict()
    assert A.alphabet == B.alphabet, "Alphabets not matching!"
    p_states = []
    p_start = None
    p_end = []
    p_var = dict()

    # Create states for Product Automaton
    for state_A in A.states:
        for state_B in B.states:
            Name = state_A.name + '_' + state_B.name
            p_var[Name] = state(Name)

    # Add transition rules for Product Automaton
    for state_A in A.states:
        for state_B in B.states:
            Name = state_A.name + '_' + state_B.name
            for letter in A.alphabet:
                next_state = state_A.transit[letter].name + '_' + state_B.transit[letter].name
                p_var[Name].transit[letter] = p_var[next_state]

    # Add states of Product Automaton to list
    for state in p_var:
        p_states.append(p_var[state])

    # Add start state of Product Automaton
    p_start = p_var[A.start.name + '_' + B.start.name]

    # Add end states of Product Automaton to list
    for end_state_A in A.end:
        for end_state_B in B.end:
            p_end.append(p_var[end_state_A.name + '_' + end_state_B.name])

    # return Product Automaton
    return eDFA(p_name, A.alphabet, p_states, p_start, p_end)

if __name__ == '__main__':
    debug = True
    import doctest
    doctest.testmod()
