# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "matplotlib>=3.11.2",
#     "numpy>=2.5.5",
# ]
# ///

import matplotlib.pyplot as plt
import os
import numpy as np

PATH = "./mesures_MRichard_EMarron"
SAMPLE_SIZE = 5
SBOX_FILE = "./sbox_dec.txt"
PTEXT_FILE = "./pText.txt"


def init_sbox(path=SBOX_FILE):
    sbox = []
    with open(path, "r") as f:
        for line in f.readlines():
            sbox.append(int(line))
    return sbox


def init_hypothesis_matrix(path=PTEXT_FILE, sbox=init_sbox(), byte_index=0):
    return np.array(
        [
            # [
            [
                hamming_weight(sbox[n ^ bytes.fromhex(line)[byte_index]])
                for n in range(256)
            ]
            # for byte in bytes.fromhex(line)
            # ]
            for line in open(PTEXT_FILE, "r").readlines()
        ]
    )


def convert(value):
    try:
        return float(value.replace(",", "."))
    except:
        return 0.0


def hamming_weight(n):
    weight = 0
    acc = n
    for _ in range(8):
        if acc & 1 != 0:
            weight += 1
        acc >>= 1

    return weight


def main():
    sbox = init_sbox()
    # print(sbox)

    files = os.listdir(PATH)
    datasets = [[]] * 300
    for file in files:
        id = int(file.split("(")[1].split(")")[0]) - 1
        # print(id)

        data = np.loadtxt(
            PATH + "/" + file, delimiter=";", skiprows=2, converters=convert
        )
        datasets[id] = data

    # print(hamming_weight(212))
    # print(sbox[25])

    h = init_hypothesis_matrix(byte_index=0)
    h = h[:300].transpose()

    # print([dataset[0][1] for dataset in datasets])

    correlation = [
        [
            np.corrcoef(h[n], [dataset[i][1] for dataset in datasets])
            for i in range(5000)
        ]
        for n in range(len(h))
    ]
    print(correlation)

    # vector = h[:300][0]
    # print(vector)
    # print(datasets)

    # fig, axs = plt.subplots(nrows=SAMPLE_SIZE)
    # for i, data in enumerate(datasets[:SAMPLE_SIZE]):
    #     axs[i].plot(data)
    #     axs[i].set(xlabel="Temps (us)", ylabel="Canal A (mV)")
    #     axs[i].grid()
    # plt.show()


if __name__ == "__main__":
    main()
