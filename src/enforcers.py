from heapq import merge
import sys
sys.path.append("..")

class state(object):
    """ Defines a basic state with a dictionary of transitions from that state. """
    def __init__(self, name):
        self.name = name
        self.transit = dict()


class DFA(object):
    """ Class for enforcing a single property.
        
    Testable Code
    -------------
    >>> a = state('a')
    >>> b = state('b')
    >>> a.transit['0'] = b
    >>> b.transit['0'] = a
    >>> b.transit['1'] = b
    >>> a.transit['1'] = a
    >>> D = DFA('D', ['0', '1'], [a, b], a, [a])
    >>> input1 = '001010010'
    >>> D.checkAccept(input1)
    ['00', '1', '010', '010']
    >>> input2 = '000'
    >>> D.checkAccept(input2)
    ['00']
    >>> input3 = '0100110'
    >>> D.checkAccept(input3)
    ['00', '1', '00', '1', '1']
    >>> input4 = '111'
    >>> D.checkAccept(input4)
    []
    >>> input5 = '0010'
    >>> D.checkAccept(input5)
    ['01110', '010']
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

    def runInput(self, _input):
        """ Runs the given input instance through the automata starting at the current state updated from the previous input. """
        self.buffer.append(_input)
        self.curr_state = self.curr_state.transit[_input]
        var = self.curr_state
        if var in self.end:
            self.buffer = [] # Flush Internal Buffer
        return var

    def checkAccept(self, _input):
        """ Checks whether the input in accepted by the automaton. """
        index = []
        output = []
        buffer_on_flush = ''
        if self.buffer:
            buffer_on_flush = ''.join(self.buffer)
        for idx, i in enumerate(_input):
            State = self.runInput(i)
            if State in self.end:
                index.append(idx)
        if index:
            output.append(buffer_on_flush + _input[: index[0] + 1])
            for i in range(len(index) - 1):
                output.append(_input[index[i] + 1 : index[i + 1] + 1])
        return output

    def __flushBuffer(self):
        """ Flushes the contents of the buffer. Only emergency use. """
        self.buffer = []


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
    ['00', '1', '00', '1', '1']
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
    This merge technique works for all regular properties.
    
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
        """ Returns stream of outputs accepted by the parallel composition. """
        for i in Input:
            signal = self.updateStatusOnInput(i)
            self.maxMerge(signal)
        return self.output


class maximal_prefix_parallel_enforcer(object):
    """ Class for maximal prefix parallel enforcer. This merge technique does not work for all regular properties.

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
    >>> M = maximal_prefix_parallel_enforcer(A, B)
    >>> M.checkAccept(t)
    ['110110011', '101101']
    >>> t = 'abc'
    >>> A1, A2, A3 = state('A1'), state('A2'), state('A3')
    >>> B1, B2, B3, B4, B5 = state('B1'), state('B2'), state('B3'), state('B4'), state('B5')
    >>> A1.transit['a'] = A2
    >>> A1.transit['b'] = A3
    >>> A1.transit['c'] = A3
    >>> A2.transit['a'] = A3
    >>> A2.transit['b'] = A1
    >>> A2.transit['c'] = A1
    >>> A3.transit['a'] = A3
    >>> A3.transit['b'] = A3
    >>> A3.transit['c'] = A3
    >>> B1.transit['a'] = B2
    >>> B1.transit['b'] = B5
    >>> B1.transit['c'] = B5
    >>> B2.transit['a'] = B5
    >>> B2.transit['b'] = B3
    >>> B2.transit['c'] = B5
    >>> B3.transit['a'] = B5
    >>> B3.transit['b'] = B5
    >>> B3.transit['c'] = B4
    >>> B4.transit['a'] = B4
    >>> B4.transit['b'] = B4
    >>> B4.transit['c'] = B4
    >>> B5.transit['a'] = B5
    >>> B5.transit['b'] = B5
    >>> B5.transit['c'] = B5
    >>> A = pDFA('A', ['a', 'b', 'c'], [A1, A2, A3], A1, [A1])
    >>> B = pDFA('B', ['a', 'b', 'c'], [B1, B2, B3, B4, B5], B1, [B4])
    >>> M = maximal_prefix_parallel_enforcer(A, B)
    >>> M.checkAccept(t)
    ['ab']
    """
    def __init__(self, *D):
        """
        Initializes enforcers for input verification of the maximal prefix parallel composition.

        Args
        ----
        *D     : set of parallel enforcer automaton (should be atleast 2 lest AssertionError).
        """
        assert len(D) > 1, "Too few DFA to combine"
        self.D = D
        self.output = []
        self.enforcer_outputs = ['' for _ in D]
        self.total_enforcer_count = len(D)

    def updateStatusOnInput(self, _input):
        """
        Updates output arrays after processing current input character for each parallel enforcers.
        """
        for idx, automata in enumerate(self.D):
            output = automata.checkAccept(_input)
            self.enforcer_outputs[idx] += ''.join(output)

    def maximalPrefixMerge(self):
        """
        Computes and returns the maximal prefix from the output arrays.
        """
        if any([output == '' for output in self.enforcer_outputs]):
            return ''
        mergeResult = min(self.enforcer_outputs)
        mergeResult_len = len(mergeResult)
        if mergeResult != '':
            self.enforcer_outputs = [self.enforcer_outputs[i][mergeResult_len : ] for i in range(self.total_enforcer_count)]
            self.output.append(mergeResult)

    def checkAccept(self, Input):
        """ Returns stream of outputs accepted by the parallel composition. """
        for i in Input:
            self.updateStatusOnInput(i)
            self.maximalPrefixMerge()
        return self.output


class serial_composition_enforcer(object):
    """ Class for generating a serial composition of enforcers.
    
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
    >>> A = DFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])
    >>> B = DFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])
    >>> M = serial_composition_enforcer(A, B)
    >>> M.checkAccept(t)
    ['110110011', '101101']
    >>> N = serial_composition_enforcer(B, A)
    >>> N.checkAccept(t)
    ['110110011', '101101']
    >>> t = 'abac'
    >>> A1, A2, A3 = state('A1'), state('A2'), state('A3')
    >>> B1, B2, B3, B4, B5 = state('B1'), state('B2'), state('B3'), state('B4'), state('B5')
    >>> A1.transit['a'] = A2
    >>> A1.transit['b'] = A3
    >>> A1.transit['c'] = A3
    >>> A2.transit['a'] = A3
    >>> A2.transit['b'] = A1
    >>> A2.transit['c'] = A1
    >>> A3.transit['a'] = A3
    >>> A3.transit['b'] = A3
    >>> A3.transit['c'] = A3
    >>> B1.transit['a'] = B2
    >>> B1.transit['b'] = B5
    >>> B1.transit['c'] = B5
    >>> B2.transit['a'] = B5
    >>> B2.transit['b'] = B3
    >>> B2.transit['c'] = B5
    >>> B3.transit['a'] = B4
    >>> B3.transit['b'] = B5
    >>> B3.transit['c'] = B5
    >>> B4.transit['a'] = B5
    >>> B4.transit['b'] = B5
    >>> B4.transit['c'] = B1
    >>> B5.transit['a'] = B5
    >>> B5.transit['b'] = B5
    >>> B5.transit['c'] = B5
    >>> A = DFA('A', ['a', 'b', 'c'], [A1, A2, A3], A1, [A1])
    >>> B = DFA('B', ['a', 'b', 'c'], [B1, B2, B3, B4, B5], B1, [B4])
    >>> M = serial_composition_enforcer(A, B)
    >>> M.checkAccept(t)
    ['aba']
    >>> A._DFA__flushBuffer() # Only for independent testing
    >>> B._DFA__flushBuffer() # Only for independent testing
    >>> N = serial_composition_enforcer(B, A)
    >>> N.checkAccept(t)
    ['ab']
    """
    def __init__(self, *D):
        """
        Initializes enforcers for input verification of the serial composition.
        Args
        ----
        *D     : set of enforcer automaton (should be atleast 1 lest AssertionError).
        """
        assert len(D) > 0, "No input DFA"
        self.output = []
        self.D = D

    def updateStatusOnInput(self, _input):
        """
        Returns the emitted output after processing current input character for each of the enforcers sequentially.
        """
        output = _input
        for automata in self.D:
            if output != '':
                output = ''.join(automata.checkAccept(output))
                continue
            break
        return output

    def checkAccept(self, Input):
        """ Returns stream of outputs accepted by the serial composition. """
        for i in Input:
            output_on_token = self.updateStatusOnInput(i)
            if output_on_token:
                self.output.append(output_on_token)
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
