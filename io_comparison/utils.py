from dataclasses import dataclass
from typing import Dict, Tuple

from PIL import ImageColor

from io_comparison.settings import CLASSES_SPECS


@dataclass
class ClassSpecIndex:
    class_idx: int
    num_classes: int

    spec_idx: int
    num_specs: int

    global_idx: int
    num_global: int


def build_class_spec_inds() -> Dict[str, Dict[str, ClassSpecIndex]]:

    inds_info = {
        class_: {
            spec: get_class_spec_inds(class_, spec) for spec in specs
        }
        for class_, specs in CLASSES_SPECS.items()
    }
    return inds_info


def get_class_spec_inds(class_: str, spec: str) -> ClassSpecIndex:

    class_idx = list(CLASSES_SPECS.keys()).index(class_)
    num_classes = len(CLASSES_SPECS)

    spec_idx = CLASSES_SPECS[class_].index(spec)
    num_specs = len(CLASSES_SPECS[class_])

    # When flattening out the specs, need to build a list of unique (class, spec) combinations. Otherwise we will run
    # into issues where a single spec can refer to multiple classes (e.g. "Holy" could be Paladin or Priest).
    flattened = []
    for this_class, specs in CLASSES_SPECS.items():
        class_specs = [(this_class, spec) for spec in specs]
        flattened.extend(class_specs)

    global_idx = flattened.index((class_, spec))
    num_global = len(flattened)

    return ClassSpecIndex(class_idx, num_classes, spec_idx, num_specs, global_idx, num_global)


def get_text_color(background_color: str) -> str:
    """
    Input and output are hex-codes.

    References
    ----------
    https://stackoverflow.com/questions/1855884/determine-font-color-based-on-background-color

    FIXME: Update docstring and comments.
    """

    rgb_background = ImageColor.getcolor(background_color, "RGB")

    # Calculate the perceptive luminance.
    luma = ((0.299 * rgb_background[0]) + (0.587 * rgb_background[1]) + (0.114 * rgb_background[2])) / 255

    # Return black for bright colors, white for dark colors.
    if luma > 0.5:
        return ("#000000", "#FFFFFF")
    else:
        return ("#FFFFFF", "#000000")
