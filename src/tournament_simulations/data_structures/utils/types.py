from typing import Mapping

# maps each possible result (string) to its probability
ResultProbability = Mapping[str, float]

# maps (points gained by home team, points gained by away team) to its probability
PontuationProbability = Mapping[tuple[float, float], float]

Probability = ResultProbability | PontuationProbability
