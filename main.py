# main.py - runs both A* algorithms on test maps and compares results
# run with: python3 main.py

import os
from utils          import ALL_MAPS, path_length
from astar          import astar
from enhanced_astar import enhanced_astar
from visualization  import plot_comparison

SAVE_FIGURES = True   # set to False to show interactive windows instead
OUTPUT_DIR   = "results"


def run_experiment(map_fn):
    grid, start, goal, name = map_fn()

    print(f"\n{'='*55}")
    print(f"  {name}  |  Grid: {grid.shape[0]}x{grid.shape[1]}  |  "
          f"Start: {start}  Goal: {goal}")
    print(f"{'='*55}")

    # run standard A*
    path_s, nodes_s, time_s, exp_s = astar(grid, start, goal)
    len_s = path_length(path_s) if path_s else 0

    # run enhanced A* (with turn and proximity penalties)
    path_e, nodes_e, time_e, exp_e = enhanced_astar(grid, start, goal)
    len_e = path_length(path_e) if path_e else 0

    # print comparison table
    print(f"  {'Metric':<22} {'Standard A*':>15} {'Enhanced A*':>15}")
    print(f"  {'-'*52}")
    print(f"  {'Path length':<22} {len_s:>15.3f} {len_e:>15.3f}")
    print(f"  {'Nodes expanded':<22} {nodes_s:>15} {nodes_e:>15}")
    print(f"  {'Time (ms)':<22} {time_s*1000:>15.3f} {time_e*1000:>15.3f}")

    if path_s and path_e:
        print(f"\n  Delta path length : {len_e - len_s:+.3f}")
        print(f"  Delta nodes       : {nodes_e - nodes_s:+d}")

    # visualize
    res_std = {"path": path_s, "explored": exp_s, "nodes": nodes_s,
               "time": time_s, "length": len_s}
    res_enh = {"path": path_e, "explored": exp_e, "nodes": nodes_e,
               "time": time_e, "length": len_e}

    save_path = None
    if SAVE_FIGURES:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        fname = name.replace(" ", "_").replace("/", "_") + ".png"
        save_path = os.path.join(OUTPUT_DIR, fname)

    plot_comparison(grid, res_std, res_enh, name, save_path)


if __name__ == "__main__":
    print("Shortest Path Finder: Standard A* vs Enhanced A*")
    print("Intro to Algorithms - Course Project")
    for map_fn in ALL_MAPS:
        run_experiment(map_fn)
    print(f"\nAll done. Figures saved to '{OUTPUT_DIR}/'")
