from pandas import DataFrame
import numpy as np
import cv2
from network import test_frcnn
from optparse import OptionParser
import os
import os.path
from solver import solve_sodoku
import urllib.request


def solve(blob):
    def generate_row(row):
        to_ret = []

        line = sorted(row, key=lambda x: x[0])
        line.insert(0, (0, 0, '-'))
        line.append((600, 0, '-'))
        for j, _ in enumerate(line):
            if j > 0:
                to_ret.append('0' * int(round((line[j][0] - line[j - 1][0]) / m_lengths) - 1))
                to_ret.append(line[j][2])

        return list(map(int, ''.join(to_ret[:-1])))

    calculations = test_frcnn.calculations(blob)

    lengths = []
    heights = []
    solve = []

    for line in calculations:
        line = line.split(',')
        side = (int(line[3]) - int(line[1])) / 2
        solve.append((
            int(line[1]) + side,
            int(line[2]) + side,
            line[5]
        ))
        lengths.append((int(line[3]) - int(line[1])))
        heights.append((int(line[4]) - int(line[2])))

    m_lengths = np.mean(lengths)
    m_heights = np.mean(heights)

    solve.sort(key=lambda x: x[1])

    row = []
    puzzle = []
    for i, _ in enumerate(solve):
        if i > 0:
            if solve[i][1] - solve[i-1][1] > 0.5 * m_heights:
                puzzle.append(generate_row(row))
                row = []
        row.append(solve[i])
    puzzle.append(generate_row(row))

    # draw output
    x = [i for i in range(30, 600, 66)]
    y = [i for i in range(40, 600, 66)]
    img = np.zeros((600, 600, 3), dtype='uint8')
    cv2.line(img, (198, 0), (198, 600), (255, 255, 255))
    cv2.line(img, (396, 0), (396, 600), (255, 255, 255))
    cv2.line(img, (0, 198), (600, 198), (255, 255, 255))
    cv2.line(img, (0, 396), (600, 396), (255, 255, 255))

    for r, row in enumerate(solve_sodoku(np.array(puzzle))):
        for c, cell in enumerate(map(str, map(int, row))):
            cv2.putText(img, cell, (x[c], y[r]), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

    cv2.imwrite(os.path.join(os.getcwd(), 'output', blob), 255-img)


if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-p", "--path", dest="test", help="Test File Name", default='test.jpg')
    (options, _) = parser.parse_args()

    if not os.path.exists('model_frcnn.hdf5'):
        print('Downloading Model Weights')
        urllib.request.urlretrieve('https://storage.googleapis.com/sodoku-240419/model_frcnn.hdf5', 'model_frcnn.hdf5')

    solve(options.test)
