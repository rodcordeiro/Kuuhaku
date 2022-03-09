import logging
from bot import Bot
from db import Database
from Trello import Trello

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Kuuhaku")

logger.info("Start application")
Database().prepare()
client = Bot().run()

