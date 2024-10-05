from loguru import logger
from time import sleep
import os


def do_something(
    text: str = "Default text", sleep_period: int = 5, repetitions: int = 5
):
    if not repetitions:
        logger.warning("No repetitions detected, exiting...")
        return

    for rep in repetitions:
        logger.info(f"{text}: {rep}/{repetitions}")
        sleep(sleep_period)

    logger.info(f"completed {repetitions} reps of {text} @ {sleep_period}s per cycle")


if __name__ == "__main__":
    text = os.getenv("TEXT")
    sleep_period = int(os.getenv("SLEEP_PERIOD"))
    repetitions = int(os.getenv("REPETITIONS"))
