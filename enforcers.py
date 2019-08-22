from automata import *

class pDFA(DFA):
    """ Class for enforcing a single property through parallel composition.
        
    Testable Code
    -------------
    >>> a = state('a')
    >>> b = state('b')
    >>> a.transit['0'] = b
    >>> b.transit['0'] = a
    >>> b.transit['1'] = b
    >>> a.transit['1'] = a
    >>> D = pDFA('D', ['0', '1'], [a, b], a, [a])
    >>> input1 = '001010010'
    >>> D.checkAccept(input1)
    ['00', '1', '010', '010']
    >>> D.outBuffer()
    ['0', '0', '1', '0', '1', '0', '0', '1', '0']
    >>> input2 = '000'
    >>> D.checkAccept(input2)
    ['00']
    >>> D.outBuffer()
    ['0', '0', '1', '0', '1', '0', '0', '1', '0', '0', '0']
    >>> input3 = '010011'
    >>> D.checkAccept(input3)
    ['0', '1', '00', '1', '1']
    >>> D.outBuffer()
    ['0', '0', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '0', '0', '1', '1']
    """
    def __init__(self, name, alphabet, states=None, start=None, end=None):
        """ Initializes necessary variables and buffers to facilitate ease of use at runtime. """
        super().__init__(name, alphabet, states, start, end)
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

    
class parallel_enforcer(object):
    """ Class for maximally merging the contents of external buffers of a set of 2 or more parallel enforcers.
    Args
    ----
    _input : String of input characters belonging to the alphabet.
    
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
    >>> M = parallel_enforcer(A, B)
    >>> M.checkAccept(t)
    ['110110011', '101101']
    """
    def __init__(self, *D):
        """
        Initializes enforcers and buffers for input verification of the parallel composition.

        Args
        ----
        *D     : set of parallel enforcer automaton (should be atleast 2 lest AssertionError).
        """
        assert len(D) > 1, "Too few DFA to combine"
        self.output = []
        self.D = D
        self.out_buffer_len = [automata.lenOut() for automata in D]

    def updateStatusOnInput(self, _input):
        """ 
        Returns a signal array where each entry suggests whether the corresponding enforcer 
        has updated its external buffer upon reading the current input character. 
        """
        signal = [0 for automata in self.D]
        for idx, automata in enumerate(self.D):
            automata.runInput(_input)
            curr_size = automata.lenOut()
            if curr_size != self.out_buffer_len[idx] and curr_size != 0:
                self.out_buffer_len[idx] = curr_size
                signal[idx] = 1
        return signal

    def maxMerge(self, signal):
        """ 
        Checks whether all enforcers have updated their external buffers upon reading the  
        current input character. If so, the output of the composition is updated and the 
        external buffers of all the enforcers are flushed. 
        """
        if all(signal) == True:
            enforced = self.D[0].outBuffer()
            for automata in self.D:
                automata.flushOutBuffer()
            self.output.append(''.join(enforced))

    def checkAccept(self, Input):
        """ Returns streams of outputs accepted by the parallel composition. """
        for i in Input:
            signal = self.updateStatusOnInput(i)
            self.maxMerge(signal)
        return self.output

    
def product(A, B, p_name):
    """ Computes the product automaton of two DFAs.

    Args
    ----
    A, B    : variables referencing a DFA.
    p_name  : name of the product automaton.

    Returns
    -------
    An DFA which is a product automaton of input DFA or A and B with name "p_name".
    
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
    >>> A = DFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    >>> B = DFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
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
    return DFA(p_name, A.alphabet, p_states, p_start, p_end)


def monolithic_enforcer(name, *D):
    """ Function for generating monolithic enforcers.
        
    Testable Code
    -------------
    >>> alpha = ['0', '1']
    >>> A1, A2, A3 = state('A1'), state('A2'), state('A3')
    >>> A1.transit['0'] = A1
    >>> A1.transit['1'] = A2
    >>> A2.transit['0'] = A3
    >>> A2.transit['1'] = A1
    >>> A3.transit['0'] = A2
    >>> A3.transit['1'] = A3
    >>> A = DFA('A', alpha, [A1, A2, A3], A1, [A1])
    >>> 
    >>> B1, B2, B3, B4, B5 = state('B1'), state('B2'), state('B3'), state('B4'), state('B5')
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
    >>> B = DFA('B', alpha, [B1, B2, B3, B4, B5], B1, [B1])
    >>> 
    >>> C1, C2, C3, C4, C5, C6, C7 = state('C1'), state('C2'), state('C3'), state('C4'), state('C5'), state('C6'), state('C7')
    >>> C1.transit['0'] = C1
    >>> C1.transit['1'] = C2
    >>> C2.transit['0'] = C3
    >>> C2.transit['1'] = C4
    >>> C3.transit['0'] = C5
    >>> C3.transit['1'] = C6
    >>> C4.transit['0'] = C7
    >>> C4.transit['1'] = C1
    >>> C5.transit['0'] = C2
    >>> C5.transit['1'] = C3
    >>> C6.transit['0'] = C4
    >>> C6.transit['1'] = C5
    >>> C7.transit['0'] = C6
    >>> C7.transit['1'] = C7
    >>> C = DFA('C', alpha, [C1, C2, C3, C4, C5, C6, C7], C1, [C1])
    >>> 
    >>> enf_property = monolithic_enforcer("Mono", A, B, C)
    >>> Input = str(bin(105*1859))[2:]
    >>> print(Input)
    101111101001111011
    >>> accept = enf_property.checkAccept(Input)
    >>> print(accept)
    ['101111101001111011']
    """
    def combine_properties(name, *D):
        assert len(D) > 1, "Too few DFA to combine"
        combined_enforcer = product(D[0], D[1], name)
        for i in range(2, len(D)):
            combined_enforcer = product(combined_enforcer, D[i], name)
        return combined_enforcer
    return combine_properties(name, *D)


if __name__ == '__main__':
    debug = True
    import doctest
    doctest.testmod()
