import matplotlib.pyplot as plt
import numpy as np

bisim = [
    88.93,
    57.06,
    39.58,
    30.11,
    24.52,
    20.88,
    18.04,
    15.94,
    14.29,
    12.98,
    12.00,
    11.16,
    10.46,
    9.80,
    9.20,
    8.71,
    8.54,
    8.43,
    8.26,
    8.06,
    7.86,
    7.72,
    7.58,
    7.44,
    7.30,
    7.13,
    7.05,
    6.89,
    6.79,
    6.68,
    6.54,
    6.48,
    6.24,
    6.17,
    6.13,
    6.06,
    5.99,
    5.99,
    5.91,
    5.87,
    5.80,
    5.74,
    5.74,
    5.68,
    5.73,
    5.57,
    5.54,
    5.65,
    5.56,
    5.56,
    5.50,
    5.48,
    5.47,
    5.42,
    5.36,
    5.34,
    5.27,
    5.33,
    5.34,
    5.23,
    5.07,
    5.06,
    5.00,
    5.03
]

diners = [
    13.46,
    10.34,
    7.22,
    5.59,
    4.57,
    3.93,
    3.34,
    3.07,
    2.67,
    2.52,
    2.28,
    2.08,
    1.95,
    1.86,
    1.71,
    1.62,
    1.56,
    1.54,
    1.47,
    1.43,
    1.40,
    1.37,
    1.33,
    1.29,
    1.27,
    1.22,
    1.20,
    1.17,
    1.14,
    1.14,
    1.11,
    1.08,
    1.22,
    1.27,
    1.28,
    1.31,
    1.28,
    1.29,
    1.30,
    1.27,
    1.29,
    1.33,
    1.28,
    1.28,
    1.26,
    1.25,
    1.24,
    1.24,
    1.23,
    1.29,
    1.24,
    1.21,
    1.31,
    1.24,
    1.21,
    1.22,
    1.29,
    1.23,
    1.21,
    1.21,
    1.31,
    1.20,
    1.24,
    1.22
]

def normalize(lst):
    maxim = max(lst)
    return [ maxim / x for x in lst ]

norm_bisim = normalize(bisim)
norm_diners = normalize(diners)

plt.figure(figsize=(5,2))
# plt.xscale("log")
# plt.xticks([1, 2, 4, 8, 16, 32, 64], ["1", "2", "4", "8", "16", "32", "64"])
plt.xlabel("#worker threads")
plt.ylabel("speed-up")
dim = np.arange(1, 65)

plt.plot(dim, norm_diners, label="diners")
plt.plot(dim, norm_bisim, label="bisim")
plt.tight_layout()

plt.legend(loc="upper left")

plt.show()
# plt.close()
