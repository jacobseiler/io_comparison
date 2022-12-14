import os
from typing import Dict, List, Optional, Union

import matplotlib
import matplotlib.pyplot as plt


class PlotHelper():
    """
    This class contains a number of useful attributes and methods to assist with creating good looking plots.
    """

    def __init__(
        self,
        colors: Optional[List[str]] = None,
        markers: Optional[List[str]] = None,
        linestyles: Optional[List[str]] = None,
        output_format: str = "png",
        output_path: str = "./plots/",
        figsize: List[float] = None,
        usetex: bool = False,
    ) -> None:
        """
        plot_output_format : string, optional
            The format of the saved plots.

        plot_output_path : string, optional
            The path where the plots will be saved. If the base directory does not exist, it will be created.
        """

        if colors is None:
            # Colours selected from colorbrewer2.org/
            colors = [
                "#e41a1c",
                "#377eb8",
                "#4daf4a",
                "#984ea3",
                "#ff7f00",
                "#cab2d6",
                "#a65628",
                "#f781bf",
                "#999999",
            ]
        self._colors = colors

        if markers is None:
            markers = [
                "x",
                "o",
                "D",
                "^",
                "s",
                "*",
                "+",
                "d",
                "<",
            ]
        self._markers = markers

        if linestyles is None:
            linestyles = ["-", "--", "-.", ":"]
        self._linestyles = linestyles

        self._output_format = output_format
        self._output_path = output_path
        self._usetex = usetex

        if figsize is None:
            figsize = [10.0, 10.0]
        self._figsize = figsize

        # Check to see if the directory exists. If ``output_path`` is "directory/tag" then we create "directory/".
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        matplotlib.rcdefaults()
        plt.rc("font", size=20)
        plt.rc("xtick", labelsize=16, direction="in")
        plt.rc("ytick", labelsize=16, direction="in")
        plt.rc("lines", linewidth=2.0)
        plt.rc("legend", numpoints=1, fontsize="x-large", handletextpad=0.1, handlelength=1.5)

        if usetex:
            plt.rc("text", usetex=usetex)

    @property
    def colors(self) -> List[str]:
        """
        list of str : the colours that will be used for plotting.
        """
        return self._colors

    @property
    def markers(self) -> List[str]:
        """
        list of str : the markers that will be used for plotting.
        """
        return self._markers

    @property
    def linestyles(self) -> List[str]:
        """
        list of str : the linestyles that will be used for plotting.
        """
        return self._linestyles

    @property
    def output_format(self) -> str:
        """
        str : the format plots will be saved as.
        """
        return self._output_format

    @property
    def output_path(self) -> str:
        """
        str : the path the plots will be saved to.
        """
        return self._output_path

    @property
    def figsize(self) -> List[float]:
        """
        str(float, float) : the size of the figures that are created.
        """
        return self._figsize

    @property
    def usetex(self) -> bool:
        """
        bool : Specifies whether to use Latex rendering for plots. If used, then need a working Latex installation.
        """
        return self.figsize

    def adjust_legend(
        self,
        ax,
        location: str = "upper right",
        scatter_plot: bool = False,
        fontsize: int = 14,
        linewidth: int = 2,
    ):
        """
        Adjusts the legend of a specified axis.

        Parameters
        ----------
        ax : ``matplotlib`` axes object
            The axis whose legend we're adjusting

        location : String, default "upper right". See ``matplotlib`` docs for full options
            Location for the legend to be placed.

        scatter_plot
            For plots involved scattered-plotted data, we adjust the size and alpha of the
            legend points.

        Returns
        -------
        None. The legend is placed directly onto the axis.
        """

        legend = ax.legend(loc=location)
        handles = legend.legendHandles

        legend.draw_frame(False)

        # First adjust the text sizes.
        for t in legend.get_texts():
            t.set_fontsize(fontsize)

        # For scatter plots, we want to increase the marker size.
        if scatter_plot:
            for handle in handles:
                # We may have lines in the legend which we don't want to touch here.
                if isinstance(handle, matplotlib.collections.PathCollection):
                    handle.set_alpha(1.0)
                    handle.set_sizes([10.0])

        for handle in handles:
            handle.set_linewidth(linewidth)

        return ax

    def update_rc_attribute(self, attribute_name: str, attribute_dict: Dict[str, Union[str, float]]) -> None:
        matplotlib.rc(attribute_name, **attribute_dict)

    def filter_latex_symbols(self, labels: Union[str, List[str]]) -> Union[str, List[str]]:

        # Not using Latex to render labels so don't need to filter or change anything.
        if not self._usetex:
            return labels

        # If passed a single string, cast it into a list so we can have consistent parsing.
        passed_was_str = False
        if isinstance(labels, str):
            labels = [labels]
            passed_was_str = True

        filtered_labels = []
        for label in labels:
            if isinstance(label, int):
                filtered_labels.append(label)
                continue

            filtered_label = label.replace("&", r"\&")  # noqa: W605
            filtered_label = filtered_label.replace("_", r"\_")  # noqa: W605
            filtered_label = filtered_label.replace("%", r"\%")  # noqa: W605

            filtered_labels.append(filtered_label)

        # We were passed a single string, recast to that before returning.
        if passed_was_str:
            filtered_labels = filtered_labels[0]

        return filtered_labels


def generate_plot_helper(**kwargs) -> PlotHelper:

    plot_helper = PlotHelper(**kwargs)
    plot_helper.update_rc_attribute("font", {"size": 36})
    plot_helper.update_rc_attribute("xtick", {"labelsize": 24})
    plot_helper.update_rc_attribute("ytick", {"labelsize": 24})
    plot_helper.update_rc_attribute("legend", {"labelspacing": 0.2})

    return plot_helper
