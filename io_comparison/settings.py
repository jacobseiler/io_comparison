from pathlib import Path

CLASSES_SPECS = {
    "death_knight": ["blood", "frost", "unholy"],
    "demon_hunter": ["havoc", "vengeance"],
    "druid": ["balance", "guardian", "feral", "restoration"],
    "hunter": ["beast_mastery", "marksmanship", "survival"],
    "mage": ["arcane", "fire", "frost"],
    "monk": ["brewmaster",  "mistweaver", "windwalker"],
    "paladin": ["holy", "protection", "retribution"],
    "priest": ["discipline", "holy", "shadow"],
    "rogue": ["assassination", "outlaw", "subtlety"],
    "shaman": ["elemental", "enhancement", "restoration"],
    "warlock": ["affliction", "demonology", "destruction"],
    "warrior": ["arms", "fury", "protection"],
}
MAX_IO = 3500
IMAGE_SIZE = 1000

CLASS_COLORS = {
    "death_knight": "#C41E3A",
    "demon_hunter": "#A330C9",
    "druid": "#FF7C0A",
    "hunter": "#AAD372",
    "mage": "#3FC7EB",
    "monk": "#00FF98",
    "paladin": "#F48CBA",
    "priest": "#FFFFFF",
    "rogue": "#FFF468",
    "shaman": "#0070DD",
    "warlock": "#8788EE",
    "warrior": "#C69B6D",
}
CURRENT_RAID = "castle-nathria"
CURRENT_RAID_BOSSES = 10
