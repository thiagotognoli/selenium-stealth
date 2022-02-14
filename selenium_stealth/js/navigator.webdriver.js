// https://github.com/berstend/puppeteer-extra/blob/c44c8bb0224c6bba2554017bfb9d7a1d0119f92f/packages/puppeteer-extra-plugin-stealth/evasions/navigator.webdriver/index.js

() => {
  if (navigator.webdriver === false) {
    // Post Chrome 89.0.4339.0 and already good
  } else if (navigator.webdriver === undefined) {
    // Pre Chrome 89.0.4339.0 and already good
  } else {
    // Pre Chrome 88.0.4291.0 and needs patching
    delete Object.getPrototypeOf(navigator).webdriver
  }
}