import logging
from pathlib import Path

NAME = "tournament_simulations_logs"
FILE = Path("./tournament_simulations_logs.log")
LEVEL = logging.WARNING

handler = logging.FileHandler(FILE)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))

tournament_simulations_logger = logging.getLogger(NAME)
tournament_simulations_logger.setLevel(LEVEL)
tournament_simulations_logger.addHandler(handler)
