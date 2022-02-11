from selenium.webdriver import Chrome as Driver
from .wrapper import add_script, evaluateOnNewDocument, send


def user_agent_override(
        driver: Driver,
        user_agent: str = None,
        language: str = None,
        platform: str = None,
        **kwargs
) -> None:
    if user_agent is None:
        ua = send(driver, "Browser.getVersion", {})['userAgent']
        # ua = driver.execute_cdp_cmd("Browser.getVersion", {})['userAgent']
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
    
    #send(driver, "Network.setUserAgentOverride", override)
    #send(driver, "Network.setUserAgentOverride", {"source": override})
    driver.execute_cdp_cmd('Network.setUserAgentOverride', override)
    #evaluateOnNewDocument(driver, 'Network.setUserAgentOverride', override)