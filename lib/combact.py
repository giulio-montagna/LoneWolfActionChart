from collections import namedtuple

import math
from math import inf
import pandas as pd

_lwDamage = pd.DataFrame(
    [[-inf, -inf, -inf, -8, -8, -6, -6, -6, -6, -5, -5, -5, -5, -5, -4, -4, -4, -4, -4, -4, -3, -3, -3],
     [-inf, -8, -8, -7, -7, -6, -6, -5, -5, -5, -5, -4, -4, -4, -3, -3, -3, -3, -3, -3, -3, -3, -2],
     [-8, -7, -7, -6, -6, -5, -5, -5, -5, -4, -4, -4, -3, -3, -3, -3, -3, -3, -2, -2, -2, -2, -2],
     [-8, -7, -7, -6, -6, -5, -5, -4, -4, -4, -4, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2],
     [-7, -6, -6, -5, -5, -4, -4, -4, -4, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1],
     [-6, -6, -6, -5, -5, -4, -4, -3, -3, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1],
     [-5, -5, -5, -4, -4, -3, -3, -2, -2, -2, -2, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0],
     [-4, -4, -4, -3, -3, -2, -2, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [-3, -3, -3, -2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    columns=list(range(-11, 12)))
_enemyDamage = [0, 0, 0, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -14, -16, -18, -inf, -inf]


def damage(combactRatio, randomNumber):
    combactRatio = max(combactRatio, -11)
    combactRatio = min(combactRatio, 11)
    assert 0 <= randomNumber <= 9, f"random number should be between 0 and 9 inclusive (got {randomNumber})"
    lwDamage = _lwDamage[combactRatio][randomNumber]
    randomOffset = randomNumber - 1 if randomNumber != 0 else 9
    damageOffset = combactRatio if combactRatio != 11 else 12
    enemyDamage = _enemyDamage[math.floor(damageOffset / 2) + 6 + randomOffset]

    return namedtuple("Damange", ["loneWolf", "enemy"])(lwDamage, enemyDamage)
