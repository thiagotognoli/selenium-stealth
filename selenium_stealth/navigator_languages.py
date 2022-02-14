from pathlib import Path
from typing import List
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


def navigator_languages(driver: Driver, languages: List[str], **kwargs) -> None:
    evaluateOnNewDocument(
        driver, Path(__file__).parent.joinpath("js/navigator.languages.js").read_text(),
        { "languages": languages },
    )
