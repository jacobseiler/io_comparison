import json
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm

from rich import print

_RAID = "castle-nathria"  # FIXME: Should be a passable argument somewhere. Should be a list of raids.

class Difficulty(Enum):
    M = "Mythic"
    H = "Heroic"
    N = "Normal"
    L = "LFR"  # TODO: See what the abbreviation for LFR is.

@dataclass
class Progression:
    number_killed: int
    number_bosses: int
    difficulty: Difficulty

@dataclass
class Profile:
    class_: str
    spec: str
    player_handle: str
    character_name: str
    character_realm: str
    region: str
    score: float
    guild: str
    progression: Dict[str, Progression]
    notes: Optional[str] = None
    special: bool = False

    def get_player_string(self) -> str:

        if self.special:
            extra = " *"
        else:
            extra = ""

        string = f"{self.character_name.title()} - {self.character_realm.title()}{extra}"
        return string


class ProfileHandler:

    _BASE_IO_URL = "https://raider.io/api/v1/characters/profile?"
    def __init__(self) -> None:
        pass

    def generate_player_profiles(
        self, fname: Optional[str] = None, data: Optional[Dict[str, Any]] = None
    ) -> List[Profile]:

        if fname is not None and data is not None:
            raise ValueError(f"Only one of `fname` and `data` can be specified.")

        if fname is not None:
            data = self._load_data(fname)

        profiles: List[Profile] = []

        for class_, class_data in tqdm(data.items()):
            for spec, spec_data in class_data.items():
                if spec_data["character_name"] == "None":
                    continue
                io_results = self._fetch_io_results(**spec_data)
                profiles.append(self._format_io_results(io_results, class_, spec, spec_data))
        return profiles

    def _format_io_results(
        self, io_results: Dict[str, Any], class_: str, spec: str, spec_data: Dict[str, str]
    ) -> Profile:

        profile = Profile(
            class_=class_,
            spec=spec,
            progression=self._get_progression(io_results),
            score=self._get_score(io_results),
            **spec_data,
        )
        return profile

    def _get_score(self, io_results: Dict[str, Any]) -> float:
        return float(io_results["mythic_plus_scores"]["all"])

    def _get_progression(self, io_results: Dict[str, Any]) -> Dict[str, Progression]:

        # TODO: Properly find an LFR example. Use Poormanrogue.
        progress = io_results["raid_progression"][_RAID]["summary"]
        difficulty = Difficulty[progress[-1]]

        # Progress is in the form "<Num Bosses Killed>/<Num Bosses Available> <Difficulty letter>"
        number_killed, number_bosses = progress[:-1].split("/")
        progression = Progression(int(number_killed), int(number_bosses), difficulty)

        # FIXME: This should iterate over raids. Is it possible to scrape older raid data to see what the pattern will
        # be?
        return {_RAID: progression}

    def _fetch_io_results(self, character_realm: str, character_name: str, region: str, **kwargs) -> Dict[str, Any]:

        # TODO: Sanitize inputs to be in correct format (lower case etc).

        # TODO: Allow ``fields`` to be customizable?
        fields = "raid_progression,mythic_plus_scores"
        response = requests.get(
            f"{self._BASE_IO_URL}region={region}&realm={character_realm}&name={character_name}&fields={fields}"
        )

        # TODO: Invalid request handling.
        return response.json()

    def _load_data(self, fname: str) -> Dict[str, Any]:

        with open(fname, "r") as f:
            data = json.load(f)
        return data
