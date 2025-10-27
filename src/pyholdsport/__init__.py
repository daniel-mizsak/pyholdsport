"""
Unofficial python library for interacting with holdsport.

@author "Daniel Mizsak" <info@pythonvilag.hu>
"""

from pyholdsport.holdsport import Holdsport
from pyholdsport.models import (
    HoldsportActivitiesUser,
    HoldsportActivity,
    HoldsportAddress,
    HoldsportMember,
    HoldsportNote,
    HoldsportRole,
    HoldsportTeam,
)

__all__ = [
    "Holdsport",
    "HoldsportActivitiesUser",
    "HoldsportActivity",
    "HoldsportAddress",
    "HoldsportMember",
    "HoldsportNote",
    "HoldsportRole",
    "HoldsportTeam",
]
