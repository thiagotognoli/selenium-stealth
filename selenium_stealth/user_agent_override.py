from selenium.webdriver import Chrome as Driver
from .wrapper import evaluateOnNewDocument
from pathlib import Path


def user_agent_override(
        driver: Driver,
        user_agent: str = None,
        language: str = None,
        platform: str = None,
        **kwargs
) -> None:
    if user_agent is None:
        ua = driver.execute_cdp_cmd("Browser.getVersion", {})['userAgent']
    else:
        ua = user_agent
    ua = ua.replace("HeadlessChrome", "Chrome")  # hide headless nature
    override = {}
    if language and platform:
        override = {"userAgent": ua, "acceptLanguage": language, "platform": platform}
    elif not language and platform:
        override = {"userAgent": ua, "acceptLanguage": language, "platform": platform}
    elif language and not platform:
        override = {"userAgent": ua, "acceptLanguage": language, "platform": platform}
    else:
        override = {"userAgent": ua}
    
    print(f"====Overwrite user agent {str(override)}")

    driver.execute_cdp_cmd('Network.setUserAgentOverride', override)
    
    evaluateOnNewDocument(
        driver, f"Network.setUserAgentOverride({str(override)})"
    )    


# def navigator_webdriver(driver: Driver, **kwargs) -> None:
#     evaluateOnNewDocument(
#         driver, Path(__file__).parent.joinpath("js/navigator.webdriver.js").read_text()
#     )
