import numpy as np
from pandas import DataFrame

def solve_sodoku(info):
    def possible(info):
        for ele in range(81):
            if info[ele // 9, ele % 9] != 0:
                yield np.array([info[ele // 9, ele % 9]])
            else:
                invalid = np.unique(np.concatenate([info[ele // 9, :],
                                                    info[:, ele % 9],
                                                    info[ele // 9 - ele // 9 % 3: ele // 9 - ele // 9 % 3 + 3,
                                                    ele % 9 - ele % 3: ele % 9 - ele % 3 + 3
                                                    ].flatten()
                                                    ]))
                yield np.array([i for i in range(1, 10) if i not in invalid])

    puzzle = DataFrame(data={'possible': [x for x in possible(info)]})

    i = 0
    mapping = np.zeros((9, 9))
    while i != 81:
        # previous mistake, backing up
        possibles = puzzle.iat[i, 0]

        if mapping[i // 9, i % 9] == np.max(possibles):
            mapping[i // 9, i % 9] = 0
            i -= 1
            continue
        else:
            set_possibles = set(possibles[np.where(possibles > mapping[i // 9, i % 9])])
            invalid = set(np.concatenate([mapping[i // 9, 0:i % 9],
                                          mapping[0:i // 9, i % 9],
                                          mapping[i // 9 - i // 9 % 3:i // 9, i % 9 - i % 3:i % 9 - i % 3 + 3].flatten()
                                          ]))

            results = set_possibles - invalid
            if len(results) == 0:
                mapping[i // 9, i % 9] = 0
                i -= 1
            else:
                mapping[i // 9, i % 9] = min(results)
                i += 1

    return mapping
