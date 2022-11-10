# Parallel Composition Runtime Enforcement
Parallel Composition Runtime Enforcement implementation in Python 3

## Imports required:
- `python >= 3.8.0` (code execution)
- `pympler >= 1.0.1` (memory traces)

## Running tests:
All tests are accessible from the **tests** folder.

### Using command-Line:
```shell
$ python3 time_tests.py
$ python3 case_study.py
```

### Using Visual Studio Code:
Run test file directly.


## Sample usage
Consider a parallel composition enforcer formed by composing two enforcers A and B. These enforce the regular properties of accepting binary strings divisible by 3 and 5 respectively.
```python
# Enforcer accepting binary strings divisible by 3

# States
A1, A2, A3 = state('A1'), state('A2'), state('A3')
# Transitions
A1.transit['0'] = A1
A1.transit['1'] = A2
A2.transit['0'] = A3
A2.transit['1'] = A1
A3.transit['0'] = A2
A3.transit['1'] = A3
# Definition (<Name>, <Alphabet>, <States>, <Start States>, <End State>)
A = pDFA('A', ['0', '1'], [A1, A2, A3], A1, [A1])

# Enforcer accepting binary strings divisible by 5

# States
B1, B2, B3, B4, B5 = state('B1'), state('B2'), state('B3'), state('B4'), state('B5')
# Transitions
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
# Definition (<Name>, <Alphabet>, <States>, <Start States>, <End State>)
B = pDFA('B', ['0', '1'], [B1, B2, B3, B4, B5], B1, [B1])

# Parallel Composition Enforcer
M = parallel_enforcer(A, B)

# Sample input string
t = str(bin(15*1859))[2:]

# Check whether input is accepted by the enforcer
# It returns the generated output stream
M.checkAccept(t)
```

Each function in the `enforcers` module is tested using a sample construction and `doctest`.
For more examples, refer individual classes and functions along with the example use cases in **tests** folder.

## Contents
- `src\`
    - `enforcers.py`
        - <span style="color:red; font-family:consolas">class</span> <span style="color:blue; font-family:consolas">state</span>
        - <span style="color:red; font-family:consolas">class</span> <span style="color:blue; font-family:consolas">DFA</span>
        - <span style="color:red; font-family:consolas">class</span> <span style="color:blue; font-family:consolas">pDFA(DFA)</span>
        - <span style="color:red; font-family:consolas">class</span> <span style="color:blue; font-family:consolas">parallel_enforcer</span>
        - <span style="color:red; font-family:consolas">class</span> <span style="color:blue; font-family:consolas">maximal_prefix_parallel_enforcer</span>
        - <span style="color:red; font-family:consolas">class</span> <span style="color:blue; font-family:consolas">serial_composition_enforcer</span>
        - <span style="color:red; font-family:consolas">function</span> <span style="color:blue; font-family:consolas">product</span>
        - <span style="color:red; font-family:consolas">function</span> <span style="color:blue; font-family:consolas">monolithic_enforcer</span>
- `tests\`
    - `test_automata.py`
    - `time_tests.py`
    - `case_study.py`
- `LICENSE`
- `README.md`

## Citation
Bibtex for citing the journal article:

```bibtex
@article{cre_fmsd_2022,
  title   = {Compositional runtime enforcement revisited},
  author  = {Pinisetty, Srinivas and Pradhan, Ankit and Roop, Partha and Tripakis, Stavros},
  journal = {Formal Methods in System Design},
  doi     = {10.1007/s10703-022-00401-y},
  year    = {2022}
}
```