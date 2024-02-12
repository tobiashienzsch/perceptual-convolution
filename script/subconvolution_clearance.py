import numpy as np


def clearance(filter_length, partitions):
    lengths = [block * segments for block, segments in partitions]
    block_size = partitions[0][0]
    assert filter_length == sum(lengths)

    prev = 0
    clearances = [0]
    for idx in range(1, len(partitions)):
        prev += lengths[idx-1]
        current_block = partitions[idx][0]
        clearances.append(int(((prev-current_block)/block_size)+1))
    return np.array(clearances)


def main():
    # n = 15872
    # p = [(512, 3), (2048, 7)]
    # n = 20992
    # p = [(128, 2), (256, 9), (2048, 9)]
    n = 36608
    p = [(128, 10), (512, 9), (2048, 15)]
    c = clearance(n, p)
    print(c)
    print(np.round(c*128/96000*1000, 2))


main()
