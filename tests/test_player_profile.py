from typing import Dict, Any, List

from io_comparison.player_profile import ProfileHandler, Profile
from io_comparison.plot import Plotter


def get_data() -> Dict[str, Any]:

    data = {
        "priest": {
            "discipline": {
                "player_handle": "Porige",
                "character_realm": "frostmourne",
                "character_name": "porige",
                "region": "US",
                "guild": "Superstars",
            },
            "holy": {
                "player_handle": "Vegan",
                "character_realm": "barthilas",
                "character_name": "veganheals",
                "region": "US",
                "guild": "Abyssal",
            },
            "shadow": {
                "player_handle": "Erod",
                "character_realm": "frostmourne",
                "character_name": "erod",
                "region": "US",
                "guild": "None",
            },
        }
    }
    return data

def mock_io_data() -> Dict[str, Any]:
    """
    Returns data in the same format that will be received from Raider IO.
    """

    data = {
        "name": "Veganheals",
        "race": "Goblin",
        "class": "Priest",
        "active_spec_name": "Holy",
        "active_spec_role": "HEALING",
        "gender": "male",
        "faction": "horde",
        "achievement_points": 14795,
        "honorable_kills": 0,
        "thumbnail_url": "https://render-us.worldofwarcraft.com/character/barthilas/218/199505114-avatar.jpg?alt=wow/static/images/2d/avatar/9-0.jpg",
        "region": "us",
        "realm": "Barthilas",
        "last_crawled_at": "2021-03-02T09:52:03.000Z",
        "profile_url": "https://raider.io/characters/us/barthilas/Veganheals",
        "profile_banner": "hordebanner1",
        "mythic_plus_scores": {"all": 925.6, "dps": 0, "healer": 925.6, "tank": 0, "spec_0": 0, "spec_1": 925.6, "spec_2": 0, "spec_3": 0},
        "raid_progression": {
            "castle-nathria": {
                "summary": "2/10 M",
                "total_bosses": 10,
                "normal_bosses_killed": 8,
                "heroic_bosses_killed": 10,
                "mythic_bosses_killed": 2
            }
        }
    }
    return data

# TODO: Put this into a class for testing the methods inside ProfileHandler
def test_io_formatting() -> None:
    handler = ProfileHandler()
    spec_data = get_data()["priest"]["holy"]
    io_data = mock_io_data()

    profile = handler._format_io_results(io_data, "priest", "holy", spec_data)

    assert profile.class_ == "priest"
    assert profile.spec == "holy"

    assert "castle-nathria" in profile.progression
    assert profile.progression["castle-nathria"].number_killed == 2
    assert profile.progression["castle-nathria"].number_bosses == 10

def test_plotting_profiles() -> None:

    handler = ProfileHandler()
    spec_data = get_data()["priest"]["holy"]
    io_data = mock_io_data()

    profile = handler._format_io_results(io_data, "priest", "holy", spec_data)
    profiles: List[Profile] = [profile]

    plotter = Plotter()
    plotter.plot_profiles(profiles, "test")


def test_generation() -> None:

    x = ProfileHandler()
    data = get_data()
    x.generate_player_profiles(data=data)
