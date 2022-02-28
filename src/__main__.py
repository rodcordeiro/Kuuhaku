import logging
from bot import Bot
from Trello import Trello

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Kuuhaku")

logger.info("Start application")
client = Bot()

