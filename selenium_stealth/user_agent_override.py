from pathlib import Path
from selenium.webdriver import Chrome as Driver
from .wrapper import add_script, evaluateOnNewDocument, evaluationString, send


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
    
    # override = {}
    # if language and platform:
    #     override = {"userAgent": ua, "acceptLanguage": language, "platform": platform}
    # elif not language and platform:
    #     override = {"userAgent": ua, "acceptLanguage": language, "platform": platform}
    # elif language and not platform:
    #     override = {"userAgent": ua, "acceptLanguage": language, "platform": platform}
    # else:
    #     override = {"userAgent": ua}
    
    # override["userAgentMetadata"] = driver.execute_script(
    #     'return '+evaluationString(
    #         Path(__file__).parent.joinpath("js/platform.js").read_text(),
    #         {"userAgent": user_agent, "language": language, "platform": platform, "maskLinux": False }
    #     )
    # )
    
    override = driver.execute_script(
        'return '+evaluationString(
            Path(__file__).parent.joinpath("js/platform.js").read_text(),
            {"userAgent": ua, "language": language, "platform": platform, "maskLinux": False }
        )
    )
    if language:
        override["acceptLanguage"] = language
     
    driver.execute_cdp_cmd('Network.setUserAgentOverride', override)
    
    # evaluateOnNewDocument(
    #     driver, Path(__file__).parent.joinpath("js/platform.js").read_text(),
    #     { "userAgent": user_agent, "language": language, "platform": platform, "maskLinux": False }
    # )
    