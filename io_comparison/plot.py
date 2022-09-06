import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import io_comparison.settings as settings
import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from rich import print
from io_comparison.generic import FloatRangeDict
from io_comparison.player_profile import Profile
from io_comparison.plot_helper import PlotHelper, generate_plot_helper
from io_comparison.utils import build_class_spec_inds, get_text_color
from matplotlib.ticker import FormatStrFormatter


class Plotter:
    """Not to be confused with the wizard."""

    _ICON_DIR = Path(__file__).parent.joinpath("../data/icons")
    _ICON_SIZE = [20, 20]  # This depends on ``IMAGE_SIZE`` to make it look nice.
    _NUM_Y_TICKS = 6
    _FIGSIZE = (24, 24)

    def __init__(self, plot_helper: Optional[PlotHelper] = None) -> None:
        self._icons: Dict[str, str] = self._get_icons()

        if plot_helper is None:
            plot_helper = generate_plot_helper(figsize=self._FIGSIZE)
        self._plot_helper = plot_helper
        self._class_spec_inds = build_class_spec_inds()
        self._progression_colors = FloatRangeDict(
            {
                (0, 0.5): "k",  # Black.
                (0.5, 0.7): "#CD7F32",  # Bronze.
                (0.7, 0.9): "#C0C0C0",  # Silver.
                (0.9, 1.01): "#FFD700",  # Gold.
            }
        )
        self._rio_icon = mpimg.imread(f"{self._ICON_DIR}/raider_io.png")

    def _snakify(self, text: str) -> str:
        x = re.sub(r"[^a-zA-Z0-9\s\-\_]", "", text.lower())
        return re.sub(r"\W", "_", x)

    def _get_icons(self) -> Dict[str, str]:

        # FIXME: Specify type.
        icons: Dict[Tuple[str, Optional[str]], Any] = {}
        for class_, specs in settings.CLASSES_SPECS.items():

            class_name = self._snakify(class_)
            icons[(class_name, None)] = mpimg.imread(f"{self._ICON_DIR}/{class_name}.jpg")

            for spec in specs:
                spec_name = self._snakify(spec)
                icons[(class_name, spec_name)] = mpimg.imread(f"{self._ICON_DIR}/{class_name}_{spec_name}.jpg")

        return icons

    def _get_x_coord(self, class_: str, spec: str) -> float:
        inds_info = self._class_spec_inds[class_][spec]

        # Add a small amount of padding.
        rel_x = (inds_info.global_idx) / (inds_info.num_global)
        return rel_x

    def _get_y_coord(self, score: float) -> float:

        # The maximum IO score will be placed at ``IMAGE_SIZE``.
        # Hence, when ``score`` == ``MAX_IO``, then this needs to return 1.
        factor = settings.IMAGE_SIZE / settings.MAX_IO
        return factor * score / settings.IMAGE_SIZE

    def _plot_class_icons(self, fig, ax) -> None:
        """
        https://stackoverflow.com/questions/24226683/using-an-image-for-tick-labels-in-matplotlib
        """

        xl, yl, xh, yh = np.array(ax.get_position()).ravel()
        w = xh - xl
        h = yh - yl

        x_offset = 0
        for class_, specs in settings.CLASSES_SPECS.items():
            inds_info = self._class_spec_inds[class_][specs[0]]

            # Generally, each class will have 3 specs. However, some have 2 and others have 4.
            # When we encounter a class with 2 specs, we need to move that class and all subsequent classes to the left
            # slightly.  When we encounter a class with 4 specs, we need to move all subsequent classes to the right
            # slightly.
            if len(specs) == 2:
                x_offset -= 0.2

            rel_x = (inds_info.class_idx + x_offset + 0.5) / (inds_info.num_classes)

            if len(specs) == 4:
                x_offset += 0.2

            xp = xl + w * rel_x
            size = 0.04

            ax1=fig.add_axes([xp-size*0.5, yl-size*1.1, size, size])
            ax1.axison = False
            imgplot = ax1.imshow(self._icons[(class_, None)])

    def _adjust_axis(self, ax) -> None:

        # Hide all spines other than the left y-axis.
        for spine in ["top", "bottom", "right"]:
            ax.spines[spine].set_visible(False)
        ax.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)

        # The actual y tick locations need to be specified based on ``IMAGE_SIZE``.
        y_ticks = np.linspace(0, settings.IMAGE_SIZE, self._NUM_Y_TICKS)
        ax.set_yticks(y_ticks)
        for tick in y_ticks[1:-1]:
            ax.axhline(tick, color="w", ls="--", lw=5, zorder=1)

        # However they should be labelled using the range of possible scores.
        y_ticks = np.linspace(0, settings.MAX_IO, self._NUM_Y_TICKS)
        ax.set_yticklabels([f"{tick:.0f}" for tick in y_ticks])

        ax.tick_params(axis="y", which="both", length=10, width=5)
        ax.spines["left"].set_linewidth(5)

    def _add_bar(self, profile: Profile, icon_coords: Tuple[float, float], ax) -> None:

        x_bar = icon_coords[0] + self._ICON_SIZE[0] / 4
        y_bar = 0
        color = settings.CLASS_COLORS[profile.class_]
        rect = patches.Rectangle(
            (x_bar, y_bar),
            width=self._ICON_SIZE[0] / 2,
            height=icon_coords[1],
            linewidth=1,
            color=color,
            zorder=2,
        )
        ax.add_patch(rect)

        if profile.score < 400:
            y_text = 1
            text_size = 8
        else:
            y_text = icon_coords[1] / 4
            text_size = 14

        x_text = icon_coords[0] + self._ICON_SIZE[0] / 4

        text = profile.get_player_string()
        text_color, outline_color = get_text_color(color)

        text = ax.text(x_text, y_text, text, rotation=90, size=text_size, color=text_color, zorder=2)
        text.set_path_effects([path_effects.Stroke(linewidth=0.5, foreground=outline_color), path_effects.Normal()])

    def _add_icon(self, profile: Profile, coords: Tuple[float, float], ax) -> None:

        x, y = coords
        extent = (x, x + self._ICON_SIZE[0], y, y + self._ICON_SIZE[1])
        imgplot = ax.imshow(self._icons[(profile.class_, profile.spec)], extent=extent, zorder=4)

    def _get_progression_color(self, profile: Profile) -> str:

        progression = profile.progression[settings.CURRENT_RAID]

        # TODO: Add check for difficulty to ensure its Mythic.
        fraction_progress = progression.number_killed / progression.number_bosses
        color = self._progression_colors[fraction_progress]
        return color

    def _add_progression(self, profile: Profile, icon_coords: Tuple[float, float], ax) -> None:

        x_box = icon_coords[0] - self._ICON_SIZE[0] * 0.16
        y_box = icon_coords[1] - self._ICON_SIZE[1] * 0.155

        color = self._get_progression_color(profile)

        rect = patches.Rectangle(
            (x_box, y_box),
            width=self._ICON_SIZE[0] * 1.3,
            height=self._ICON_SIZE[1] * 1.3,
            linewidth=1,
            color=color,
            zorder=3,
        )
        ax.add_patch(rect)

    def _add_background(self, ax, image) -> None:
        ax.set_facecolor("black")

        image_extent = [0, settings.IMAGE_SIZE, 0, settings.IMAGE_SIZE]
        ax.imshow(image, extent=image_extent, alpha=0.5)

    def _add_legend(self, ax) -> None:

        rectangles = []
        labels = []
        for progression_fraction, color in self._progression_colors.items():

            rect = patches.Rectangle((np.nan, np.nan), width=0, height=0, color=color)
            ax.add_patch(rect)
            rectangles.append(rect)

            if np.isclose(progression_fraction[0], 0.0):
                label = f"<{int(progression_fraction[1] * settings.CURRENT_RAID_BOSSES)}/{settings.CURRENT_RAID_BOSSES}M"
            else:
                label = f"{int(progression_fraction[1] * settings.CURRENT_RAID_BOSSES)}/{settings.CURRENT_RAID_BOSSES}M"
            labels.append(label)

        ax.legend(rectangles, labels)

    def plot_profiles(self, profiles: List[Profile], output_fname: str, background_image) -> None:

        print(f"Plotting scores for [bold magenta]{len(profiles)}[/] characters.")

        fig = plt.figure(figsize=self._plot_helper.figsize)
        ax = fig.add_subplot(111)

        ax.set_xlim(0, settings.IMAGE_SIZE)
        ax.set_ylim(0, settings.IMAGE_SIZE)
        ax.set_ylabel(f"Raider IO Score")

        for profile in profiles:

            x_coord = self._get_x_coord(profile.class_, profile.spec)
            y_coord = self._get_y_coord(profile.score)
            x, y = ax.transLimits.inverted().transform((x_coord, y_coord))

            self._add_icon(profile, (x, y), ax)
            self._add_bar(profile, (x, y), ax)
            self._add_progression(profile, (x, y), ax)

        self._plot_class_icons(fig, ax)
        self._adjust_axis(ax)
        self._add_background(ax, background_image)
        self._add_legend(ax)

        output_file = f"{self._plot_helper.output_path}/{output_fname}.{self._plot_helper.output_format}"
        fig.savefig(output_file, pad_inches=0)
        print(f"Saved file to [bold magenta]{output_file}[/]")
        plt.close()
