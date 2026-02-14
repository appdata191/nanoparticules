import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
'''
def graph(x, y, t, T, fps=30):

    speed  = 5
    T_end = float(T[-1])

    duration_seconds = T_end / speed
    nframes = max(2, int(np.ceil(duration_seconds * fps)))
    
    s_grid = np.linspace(0.0, T_end, nframes)

    fig1, ax1 = plt.subplots()
    line1, = ax1.plot([], [], lw=2)
    ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(min(y), max(y))
    ax1.set_title("CTRW trajectory (time-based)")

    fig2, ax2 = plt.subplots()

    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111, projection="3d")
    line3, = ax3.plot([], [], [], lw=2)
    ax3.set_title("Space-time curve (x,y,t)")
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("t")

    ax3.set_xlim(np.min(x), np.max(x))
    ax3.set_ylim(np.min(y), np.max(y))
    ax3.set_zlim(0.0, T_end)


    def idx_at_time(s):
        return int(np.searchsorted(T, s, side="right"))

    def update1(frame):
        s = s_grid[frame]
        m = idx_at_time(s)  
        if m <= 0:
            line1.set_data([], [])
        else:
            line1.set_data(x[:m], y[:m])
        return line1,

    def update2(frame):
        s = s_grid[frame]
        m = idx_at_time(s)
        ax2.clear() 

        if m > 0:
            ax2.hist(t[:m], bins=40, density=True, alpha=0.6)
        
        ax2.set_title("Waiting-time histogram (so far)")
        ax2.set_xlabel("waiting time")
        ax2.set_ylabel("density")

        return tuple(ax2.patches)
    
    def update3(frame):
        s = s_grid[frame]
        m = idx_at_time(s)
        if m <= 0:
            line3.set_data([], [])
            line3.set_3d_properties([])
        else:
            line3.set_data(x[:m], y[:m])
            line3.set_3d_properties(T[:m])
        return (line3,)

    ani1 = FuncAnimation(fig1, update1, frames=nframes)
    ani2 = FuncAnimation(fig2, update2, frames=nframes)
    ani3 = FuncAnimation(fig3, update3, frames=nframes)

    plt.show()
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def make_timeline(T, fps=30, speed=5.0):
    """Return (s_grid, idx_at_time, nframes, T_end)."""
    T_end = float(T[-1])
    duration_seconds = T_end / speed
    nframes = max(2, int(np.ceil(duration_seconds * fps)))
    s_grid = np.linspace(0.0, T_end, nframes)

    def idx_at_time(s):
        return int(np.searchsorted(T, s, side="right"))

    return s_grid, idx_at_time, nframes, T_end


def make_2d_traj_anim(x, y, s_grid, idx_at_time):
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y), np.max(y))
    ax.set_title("CTRW trajectory (time-based)")

    def update(frame):
        m = idx_at_time(s_grid[frame])
        if m <= 0:
            line.set_data([], [])
        else:
            line.set_data(x[:m], y[:m])
        return (line,)

    return fig, update


def make_hist_anim(t, s_grid, idx_at_time, bins=40):
    fig, ax = plt.subplots()
    ax.set_title("Waiting-time histogram (so far)")
    ax.set_xlabel("waiting time")
    ax.set_ylabel("density")

    def update(frame):
        m = idx_at_time(s_grid[frame])
        ax.clear()
        if m > 0:
            ax.hist(t[:m], bins=bins, density=True, alpha=0.6)
        ax.set_title("Waiting-time histogram (so far)")
        ax.set_xlabel("waiting time")
        ax.set_ylabel("density")
        return tuple(ax.patches)

    return fig, update


def make_3d_spacetime_anim(x, y, t, s_grid, idx_at_time):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    line, = ax.plot([], [], [], lw=2)

    ax.set_title("Space-time curve (x,y,t)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("t")
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y), np.max(y))
    ax.set_zlim(0.0, np.max(t))

    def update(frame):
        m = idx_at_time(s_grid[frame])
        if m <= 0:
            line.set_data([], [])
            line.set_3d_properties([])
        else:
            line.set_data(x[:m], y[:m])
            line.set_3d_properties(t[:m])
        return (line,)

    return fig, update


def graph(x, y, t, T, fps=30, speed=5.0, bins=40):
    s_grid, idx_at_time, nframes, T_end = make_timeline(T, fps=fps, speed=speed)

    fig1, upd1 = make_2d_traj_anim(x, y, s_grid, idx_at_time)
    fig2, upd2 = make_hist_anim(t, s_grid, idx_at_time, bins=bins)
    fig3, upd3 = make_3d_spacetime_anim(x, y, t, s_grid, idx_at_time)

    ani1 = FuncAnimation(fig1, upd1, frames=nframes)
    ani2 = FuncAnimation(fig2, upd2, frames=nframes)
    ani3 = FuncAnimation(fig3, upd3, frames=nframes)

    plt.show()
    return ani1, ani2, ani3