import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.patheffects import Stroke

bar_chart_heights = [0.85, 0.9, 0.85, 0.85, 0.8, 0.9]
letters = ["S", "k", "i", "m", "p", "y"]

cmap = plt.cm.magma
font = FontProperties()
font.set_name("Fira Code Bold")
txt_extra_height = 0.2


def get_logo():
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_facecolor("w")
    ax.bar(
        range(len(bar_chart_heights)),
        bar_chart_heights,
        lw=2,
        color="w",
        edgecolor="k",
        alpha=0.6,
    )
    for x in np.linspace(0, 1, 20):
        lw, color = x * 225, cmap(1 - x)
        for i, letter in enumerate(letters):
            t = ax.annotate(
                letter,
                (i, bar_chart_heights[i] + txt_extra_height),
                va="center",
                size=30,
                ha="center",
                zorder=-lw + 1,
                color="#6b5496",
            )
            t.set_path_effects([Stroke(linewidth=lw, foreground=color)])
    ax.set_ylim(None, txt_extra_height + max(bar_chart_heights))
    plt.axis("off")
    plt.show()
