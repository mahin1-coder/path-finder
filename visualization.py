# visualization.py - draw side-by-side comparison of both algorithms

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def build_image(grid, explored, path):
    # Build an RGB image: white=free, dark=obstacle, blue=explored, yellow=path
    img = np.ones((*grid.shape, 3))
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r][c] == 1:
                img[r,c] = [0.2, 0.2, 0.2]   # obstacle
    for r,c in explored:
        if grid[r][c] == 0:
            img[r,c] = [0.67, 0.84, 0.90]    # explored (light blue)
    if path:
        for r,c in path:
            img[r,c] = [1.0, 0.84, 0.1]      # path (yellow)
        img[path[0]]  = [0.18, 0.80, 0.44]   # start (green)
        img[path[-1]] = [0.90, 0.25, 0.25]   # goal (red)
    return img


def plot_comparison(grid, res_std, res_enh, title="", save_path=None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor="#f5f5f5")
    fig.suptitle(f"Shortest Path Finder  -  {title}", fontsize=13, fontweight="bold")

    labels = ["Standard A*", "Enhanced A* (turn + proximity penalties)"]
    results = [res_std, res_enh]

    for ax, res, label in zip(axes, results, labels):
        img = build_image(grid, res["explored"], res["path"])
        ax.imshow(img, origin="upper", interpolation="nearest")
        ax.set_xticks([])
        ax.set_yticks([])

        length = f"{res['length']:.2f}" if res["path"] else "N/A"
        ax.set_title(
            f"{label}\nLength: {length}  |  Nodes: {res['nodes']}  |  Time: {res['time']*1000:.2f}ms",
            fontsize=9, fontweight="bold", pad=8
        )

        # legend
        patches = [
            mpatches.Patch(facecolor=[1,1,1],           edgecolor="gray", label="Free"),
            mpatches.Patch(facecolor=[0.2,0.2,0.2],                        label="Obstacle"),
            mpatches.Patch(facecolor=[0.67,0.84,0.90],                     label="Explored"),
            mpatches.Patch(facecolor=[1.0,0.84,0.1],                       label="Path"),
            mpatches.Patch(facecolor=[0.18,0.80,0.44],                     label="Start"),
            mpatches.Patch(facecolor=[0.90,0.25,0.25],                     label="Goal"),
        ]
        ax.legend(handles=patches, loc="lower left", fontsize=7.5, ncol=2, framealpha=0.9)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {save_path}")
    else:
        plt.show()
    plt.close(fig)
