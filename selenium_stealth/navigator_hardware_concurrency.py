from pathlib import Path
from .wrapper import evaluateOnNewDocument
from selenium.webdriver import Chrome as Driver


def navigator_hardware_concurrency(driver: Driver, hardwareConcurrency: str, **kwargs) -> None:
    evaluateOnNewDocument(
        driver, Path(__file__).parent.joinpath("js/navigator.hardwareConcurrency.js").read_text(), {"hardwareConcurrency": hardwareConcurrency}
    )
