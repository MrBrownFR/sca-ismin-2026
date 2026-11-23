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
from multiprocessing import Pool

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


def find_key_for_byte(datasets, byte_index, samples=5000):
    h = init_hypothesis_matrix(byte_index=byte_index)
    h = h[:300].transpose()

    # print([dataset[0][1] for dataset in datasets])

    correlations = [
        [
            np.corrcoef(h[n], [dataset[i][1] for dataset in datasets])[0][1]
            for i in range(samples)
        ]
        for n in range(len(h))
    ]
    # print(correlations)

    arg = np.argmax(correlations)
    # print(
    #     f"Octet {i + 1}: clé {hex(int(arg / samples))}, indice {arg % samples}, coef {correlations[int(arg / samples)][arg % samples]}"
    # )

    return (
        int(arg / samples),
        arg % samples,
        correlations[int(arg / samples)][arg % samples],
    )


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

    global f

    def f(i):
        find_key_for_byte(datasets, i, samples=5000)

    with Pool() as p:
        results = p.starmap(
            find_key_for_byte,
            [(datasets, i) for i in range(16)],
        )
    for i, result in enumerate(results):
        # print(result)
        key, index, correl = result
        print(f"Octet {i + 1}: clé {hex(key)}, indice {index}, coef {correl}")

    # for i in range(16):
    #     h = init_hypothesis_matrix(byte_index=i)
    #     h = h[:300].transpose()

    #     # print([dataset[0][1] for dataset in datasets])

    #     correlations = [
    #         [
    #             np.corrcoef(h[n], [dataset[i][1] for dataset in datasets])[0][1]
    #             for i in range(SAMPLES)
    #         ]
    #         for n in range(len(h))
    #     ]
    #     # print(correlations)

    #     arg = np.argmax(correlations)
    #     print(
    #         f"Octet {i + 1}: clé {hex(int(arg / SAMPLES))}, indice {arg % SAMPLES}, coef {correlations[int(arg / SAMPLES)][arg % SAMPLES]}"
    #     )


if __name__ == "__main__":
    main()
