from graphic import graph
from model import CTRW
import numpy as np

def main():
    lambda_ = 1
    tau0 = 0.2
    alpha = 0.6
    mean = 0.0
    std = 5.0
    steps = 300

    x, y, t, T = CTRW(lambda_, tau0, alpha, mean, std, steps, waiting_type="exp", rng=np.random.default_rng())

    graph(x=x, y=y, t=t, T=T)

if __name__ == "__main__":
    main()