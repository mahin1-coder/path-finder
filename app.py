# app.py - Streamlit web app for the Shortest Path Finder project
# run locally with: streamlit run app.py

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import time

from utils import make_map1, make_map2, make_map3, path_length
from astar import astar
from enhanced_astar import enhanced_astar


# ---- page config ----
st.set_page_config(page_title="Shortest Path Finder", layout="wide", page_icon="🗺️")

st.title("🗺️ Shortest Path Finder")
st.markdown("**Comparative Analysis: Standard A\* vs Enhanced A\***")
st.markdown("Select a map, adjust the penalty weights, and hit **Run** to compare both algorithms.")
st.divider()


# ---- sidebar controls ----
st.sidebar.header("⚙️ Settings")

map_choice = st.sidebar.selectbox(
    "Select Map",
    ["Map 1 — Open Field", "Map 2 — Narrow Corridor", "Map 3 — Dense Clutter"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Enhanced A* Parameters")
alpha = st.sidebar.slider("Turn Penalty (alpha)", 0.0, 2.0, 0.5, 0.1,
                           help="Higher = smoother, less turning")
beta  = st.sidebar.slider("Proximity Penalty (beta)", 0.0, 2.0, 0.4, 0.1,
                           help="Higher = more clearance from walls")
radius = st.sidebar.slider("Obstacle Scan Radius", 1, 4, 2, 1,
                            help="How many cells around each node to check for walls")

run = st.sidebar.button("▶ Run Comparison", use_container_width=True, type="primary")


# ---- load selected map ----
map_fns = {
    "Map 1 — Open Field":      make_map1,
    "Map 2 — Narrow Corridor": make_map2,
    "Map 3 — Dense Clutter":   make_map3,
}
grid, start, goal, name = map_fns[map_choice]()


# ---- helper: build RGB image ----
def build_image(grid, explored, path):
    img = np.ones((*grid.shape, 3))
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r][c] == 1:
                img[r, c] = [0.2, 0.2, 0.2]
    for r, c in explored:
        if grid[r][c] == 0:
            img[r, c] = [0.67, 0.84, 0.90]
    if path:
        for r, c in path:
            img[r, c] = [1.0, 0.84, 0.1]
        img[path[0]]  = [0.18, 0.80, 0.44]
        img[path[-1]] = [0.90, 0.25, 0.25]
    return img


# ---- helper: draw one panel ----
def draw_panel(ax, grid, explored, path, title):
    img = build_image(grid, explored, path)
    ax.imshow(img, origin="upper", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    patches = [
        mpatches.Patch(facecolor=[1,1,1],          edgecolor="gray", label="Free"),
        mpatches.Patch(facecolor=[0.2,0.2,0.2],                       label="Obstacle"),
        mpatches.Patch(facecolor=[0.67,0.84,0.90],                    label="Explored"),
        mpatches.Patch(facecolor=[1.0,0.84,0.1],                      label="Path"),
        mpatches.Patch(facecolor=[0.18,0.80,0.44],                    label="Start"),
        mpatches.Patch(facecolor=[0.90,0.25,0.25],                    label="Goal"),
    ]
    ax.legend(handles=patches, loc="lower left", fontsize=7, ncol=2, framealpha=0.9)


# ---- show map preview before running ----
st.subheader(f"Preview: {name}")
col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Grid Size", f"{grid.shape[0]} × {grid.shape[1]}")
col_info2.metric("Start", str(start))
col_info3.metric("Goal",  str(goal))

if not run:
    # just show the empty grid as a preview
    fig_prev, ax_prev = plt.subplots(figsize=(5, 5))
    prev_img = build_image(grid, set(), None)
    # mark start/goal even before running
    prev_img[start] = [0.18, 0.80, 0.44]
    prev_img[goal]  = [0.90, 0.25, 0.25]
    ax_prev.imshow(prev_img, origin="upper", interpolation="nearest")
    ax_prev.set_xticks([])
    ax_prev.set_yticks([])
    ax_prev.set_title("Grid preview (press Run to start)", fontsize=10)
    st.pyplot(fig_prev, use_container_width=False)
    plt.close(fig_prev)
    st.info("👈 Adjust settings in the sidebar and press **▶ Run Comparison** to start.")


# ---- run algorithms when button pressed ----
if run:
    with st.spinner("Running Standard A*..."):
        path_s, nodes_s, time_s, exp_s = astar(grid, start, goal)
        len_s = path_length(path_s) if path_s else 0

    with st.spinner("Running Enhanced A*..."):
        path_e, nodes_e, time_e, exp_e = enhanced_astar(
            grid, start, goal, alpha=alpha, beta=beta, radius=radius
        )
        len_e = path_length(path_e) if path_e else 0

    # --- metrics row ---
    st.subheader("📊 Results Comparison")
    c1, c2, c3 = st.columns(3)
    c1.metric("Path Length",      f"{len_s:.2f}",        delta=f"{len_e-len_s:+.2f} (Enhanced)")
    c2.metric("Nodes Expanded",   f"{nodes_s}",          delta=f"{nodes_e-nodes_s:+d} (Enhanced)")
    c3.metric("Compute Time",     f"{time_s*1000:.2f}ms", delta=f"{(time_e-time_s)*1000:+.2f}ms (Enhanced)")

    st.caption("Delta values show how Enhanced A* compares to Standard A*. Positive = Enhanced used more.")

    st.divider()

    # --- side-by-side visualisation ---
    st.subheader("🖼️ Visual Comparison")
    fig, axes = plt.subplots(1, 2, figsize=(14, 7), facecolor="#f5f5f5")
    fig.suptitle(f"Shortest Path Finder  —  {name}", fontsize=13, fontweight="bold")

    draw_panel(axes[0], grid, exp_s, path_s,
               f"Standard A*\nLength: {len_s:.2f}  |  Nodes: {nodes_s}  |  Time: {time_s*1000:.2f}ms")
    draw_panel(axes[1], grid, exp_e, path_e,
               f"Enhanced A*  (α={alpha}, β={beta}, r={radius})\nLength: {len_e:.2f}  |  Nodes: {nodes_e}  |  Time: {time_e*1000:.2f}ms")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # --- explanation ---
    with st.expander("💡 What do these results mean?"):
        st.markdown(f"""
- **Standard A\*** finds the shortest raw path using only movement cost + heuristic.
- **Enhanced A\*** adds penalties for sharp turns and proximity to walls, so its path is smoother
  and keeps more distance from obstacles — but may be slightly longer and explores more nodes.
- On **{name}**, Enhanced A\* expanded **{nodes_e - nodes_s} more nodes** and produced a path
  **{len_e - len_s:+.2f} units {"longer" if len_e > len_s else "shorter"}** than the standard version.
- You can increase **alpha** to force even smoother turns, or increase **beta** to push the path
  further from walls. Try it using the sliders on the left!
        """)
