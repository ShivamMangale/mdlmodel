import numpy as np
import random

new = np.random.uniform(low=-1e-1, high=1e-2, size=(1,11))
print(new)
for l in range(11):
    ind = 0
    chpow = 0
    # print(chpow)
    while abs(new[0][l]/pow(10,-chpow)) < 1:
        chpow += 1
        # print(new[0][l])
    print(chpow, "==chpow")
    for m in range(3):
        if l+m > 10:
            break
        lo = random.randrange(-10,10)
        print(lo, " ", m)
        new[0][l+m] += lo/pow(10,chpow+m)
        new[0][l+m] = max(new[0][l+m],-10)
        new[0][l+m] = min(new[0][l+m],10)

print(new)