from loguru import logger
from time import sleep
import os


def do_something(
    text: str = "Default text", sleep_period: int = 5, repetitions: int = 5
):
    if not repetitions:
        logger.warning("No repetitions detected, exiting...")
        return

    for rep in range(repetitions):
        logger.info(f"{text}: {rep}/{repetitions}")
        sleep(sleep_period)

    logger.info(f"completed {repetitions} reps of {text} @ {sleep_period}s per cycle")


if __name__ == "__main__":
    logger.add("history.log")
    text = os.getenv("TEXT")
    sleep_period = os.getenv("SLEEP_PERIOD")
    repetitions = os.getenv("REPETITIONS")

    if text and sleep_period and repetitions:
        do_something(
            text=text, sleep_period=int(sleep_period), repetitions=int(repetitions)
        )
    else:
        logger.warning("some ENV var is missing, running with defaults")
        params = {}
        if text:
            params["text"] = text
        else:
            logger.debug("text missing, using defaults.")
        if sleep_period:
            params["sleep_period"] = int(sleep_period)
        else:
            logger.debug("sleep_period missing, using defaults.")
        if repetitions:
            params["repetitions"] = int(repetitions)
        else:
            logger.debug("repetitions missing, using defaults.")
        do_something(**params)
