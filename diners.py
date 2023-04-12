import matplotlib.pyplot as plt
import numpy as np

tlaplus_states = [ 9, 163, 1959, 22847, 287930, 3652847, 46370039 ]
tlaplus_times = [ 1, 1, 1, 1, 3, 29, 416 ]
harmony_states = [ 6, 41, 251, 1521, 9095, 53825, 315831, 1840001, 10327210 ]
harmony_times = [ 0.01, 0.01, 0.01, 0.01, 0.01, 0.04, 0.25, 2.05, 17 ]

fig, ax1 = plt.subplots(figsize=(9, 9))
ax2 = ax1.twinx()

ax1.set_yscale("log")
ax2.set_yscale("log")
# ax1.set_xlim(1, 8)
# ax2.set_xlim(1, 10)
t_dim = np.arange(1, 8)
h_dim = np.arange(1, 10)
ax1.set(xlabel="#philosophers", ylabel="#states")
ax2.set(ylabel="time (secs)")

ax1.plot(t_dim, tlaplus_states, "go-", label="#states (TLA+)")
ax1.plot(h_dim, harmony_states, "ro-", label="#states (Harmony)")
ax2.plot(t_dim, tlaplus_times, "gv-", label="time (TLA+)")
ax2.plot(h_dim, harmony_times, "rv-", label="time (Harmony)")

ax1.legend(loc="upper right")
ax2.legend(loc="upper left")

plt.show()
# plt.close()
