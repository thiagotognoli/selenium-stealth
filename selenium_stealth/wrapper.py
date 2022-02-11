from selenium.webdriver import Chrome as Driver
from typing import Any
import json


def evaluationString(fun: str, *args: Any) -> str:
    """Convert function and arguments to str."""
    _args = ', '.join([
        json.dumps('undefined' if arg is None else arg) for arg in args
    ])
    expr = '(' + fun + ')(' + _args + ')'
    return expr


def evaluateOnNewDocument(driver: Driver, pagefunction: str, *args: str) -> None:

    js_code = evaluationString(pagefunction, *args)

    add_script(driver, js_code)
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js_code,
    })
    """
    
def send(driver, cmd, params={}):
  resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
  url = driver.command_executor._url + resource
  body = json.dumps({'cmd': cmd, 'params': params})
  response = driver.command_executor._request('POST', url, body)
  print('response', response)
  # if response['status']:
    # raise Exception(response.get('value'))
  return response.get('value')

def add_script(driver, script):
  send(driver, "Page.addScriptToEvaluateOnNewDocument", {"source": script})