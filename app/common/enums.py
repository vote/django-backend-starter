from enum import EnumMeta

from enumfields import Enum


class PoliticalParty(Enum, metaclass=EnumMeta):
    NONE = "None"
    DEMOCRATIC = "Dem"
    REPUBLICAN = "GOP"
    GREEN = "Green"
    LIBERTARIAN = "Lib"
    OTHER = "Other"

    class Labels:
        DEMOCRATIC = "Democrat"
        REPUBLICAN = "Republican"
        LIBERTARIAN = "Libertarian"
