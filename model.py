import numpy as np

def exp_t(lambda_, rng):
    p = rng.uniform(0,1)
    return -(1/lambda_) * np.log(p)

def power_t(tau0, alpha, rng):
    p = rng.uniform(0,1)
    return tau0 * (p ** (-1/alpha))

def gaussian_x(mean, std, rng):
    return rng.normal(loc=mean, scale=std, size=2)

def CTRW(lambda_, tau0, alpha, mean, std, steps, waiting_type: str, rng):
    if waiting_type not in ("exp", "power"):
        raise ValueError("waiting_type is 'exp' or 'power'")
    x = np.zeros(steps)
    y = np.zeros(steps)
    t = np.zeros(steps)

    for i in range(steps):
        dx, dy = gaussian_x(mean, std, rng)
        if i ==0:
            x[i], y[i] = dx, dy
        else:
            x[i] = x[i-1] + dx
            y[i] = y[i-1] + dy

        if waiting_type == "exp":
            t[i] = exp_t(lambda_, rng)
        else:
            t[i] = power_t(tau0, alpha, rng)
        
        print(f"Step {i+1}/{steps}: x={x[i]:.2f}, y={y[i]:.2f}, t={t[i]:.2f}")
    
    T = np.cumsum(t)
    return x,y,t, T
