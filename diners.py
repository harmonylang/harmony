import matplotlib.pyplot as plt
import numpy as np

tlaplus_states = [ 9, 163, 1959, 22847, 287930, 3652847, 46370039 ]
tlaplus_times = [ 1, 3, 29, 416 ]
harmony_states = [ 6, 41, 251, 1521, 9095, 53825, 315831, 1840001, 10327210 ]
harmony_times = [ 0.01, 0.04, 0.25, 2.05, 17 ]

fig, ax1 = plt.subplots(figsize=(6, 3))
ax2 = ax1.twinx()

ax1.set_yscale("log")
ax2.set_yscale("log")
# ax1.set_xlim(1, 8)
# ax2.set_xlim(1, 10)
ts_dim = np.arange(1, 8)
tt_dim = np.arange(4, 8)
hs_dim = np.arange(1, 10)
ht_dim = np.arange(5, 10)
ax1.set(xlabel="#philosophers", ylabel="#states")
ax2.set(ylabel="time (secs)")
ax2.set_yticks([0.01, 0.1, 1, 10, 100], labels=["0.01", "0.1", "1", "10", "100"])

ax1.plot(ts_dim, tlaplus_states, "go-", label="#states (TLA+)")
ax1.plot(hs_dim, harmony_states, "ro-", label="#states (Symphony)")
ax2.plot(tt_dim, tlaplus_times, "gv-", label="time (TLA+)")
ax2.plot(ht_dim, harmony_times, "rv-", label="time (Symphony)")

ax1.legend(loc="upper left", bbox_to_anchor=(0, 1))
ax2.legend(loc="upper left", bbox_to_anchor=(0, 0.8))

plt.tight_layout()
plt.show()
# plt.close()
