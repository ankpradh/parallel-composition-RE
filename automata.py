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
    >>> input3 = '010011'
    >>> D.checkAccept(input3)
    ['0', '1', '00', '1', '1']
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
        for idx, i in enumerate(_input):
            State = self.runInput(i)
            if State in self.end:
                index.append(idx)
        if index:
            output.append(_input[: index[0] + 1])
            for i in range(len(index) - 1):
                output.append(_input[index[i] + 1 : index[i + 1] + 1])
        return output


if __name__ == '__main__':
    debug = True
    import doctest
    doctest.testmod()
