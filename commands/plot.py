import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.image as mpimg
from rich.console import Console

from io_comparison.player_profile import ProfileHandler
from io_comparison.plot import Plotter

console = Console()


def get_data(fname: str) -> Dict[str, Any]:
    with open(fname, "r") as f_in:
        data = json.load(f_in)
    return data

def get_image(tag: str):


    for image_format in ["png", "jpg"]:
        fname = Path(__file__).parent.joinpath(f"../data/icons/{tag}.{image_format}")

        try:
            image = mpimg.imread(fname)
        except FileNotFoundError:
            continue
        else:
            break

    return image

def get_data_fname() -> Tuple[str, str, Optional[Any]]:
    tag = console.input(
        f"Enter in the [bold red]data JSON file[/] you wish compare.\n"
        f"Enter [bold cyan]wowhead[/] to compare the authors of Wowhead class guides.\n"
        f"Enter [bold cyan]icy[/] to compare the authors of the Icy Veins class guides.\n"
    )
    print("")

    if tag == "wowhead":
        fname = Path(__file__).parent.joinpath("../data/wowhead.json")
        tag = "wowhead"
        extra_image = get_image("wowhead")
    elif tag == "icy":
        fname = Path(__file__).parent.joinpath("../data/icy_veins.json")
        tag = "icy"
        extra_image = get_image("icy_veins")
    else:
        fname = tag
        tag = "user"
        extra_image = None

    return fname, tag, extra_image


if __name__ == "__main__":

    handler = ProfileHandler()
    fname, tag, extra_image = get_data_fname()

    data = get_data(fname)
    profiles = handler.generate_player_profiles(data=data)

    plotter = Plotter()
    plotter.plot_profiles(profiles, tag, extra_image)
