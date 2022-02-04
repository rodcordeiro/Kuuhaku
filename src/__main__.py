from decouple import config
import logging
from bot import Bot, Client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Kuuhaku")

logger.info("Start application")
client = Bot()