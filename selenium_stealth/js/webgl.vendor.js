// https://github.com/berstend/puppeteer-extra/blob/c44c8bb0224c6bba2554017bfb9d7a1d0119f92f/packages/puppeteer-extra-plugin-stealth/evasions/webgl.vendor/index.js

(opts) => {
  try {
    const stripErrorStack = (stack) => stack
      .split('\n')
      .filter((line) => !line.includes('at Object.apply'))
      .filter((line) => !line.includes('at Object.get'))
      .join('\n');

    const getParameterProxyHandler = {
      get(target, key) {
        try {
          // Mitigate Chromium bug (#130)
          if (typeof target[key] === 'function') {
            return target[key].bind(target);
          }
          return Reflect.get(target, key);
        } catch (err) {
          err.stack = stripErrorStack(err.stack);
          throw err;
        }
      },
      apply(target, thisArg, args) {
        const param = (args || [])[0];
        // UNMASKED_VENDOR_WEBGL
        if (param === 37445) {
          return opts.vendor || 'Intel Inc.';
        }
        // UNMASKED_RENDERER_WEBGL
        if (param === 37446) {
          return opts.renderer || 'Intel Iris OpenGL Engine';
        }
        try {
          return utils.cache.Reflect.apply(target, thisArg, args);
        } catch (err) {
          err.stack = stripErrorStack(err.stack);
          throw err;
        }
      },
    };

    // console.log('opts1')
    // console.log(opts)
    const __getParameterProxyHandler = {
      apply: function (target, ctx, args) {
        const param = (args || [])[0]
        const result = utils.cache.Reflect.apply(target, ctx, args)

        // if (result == null) {
        //   // console.log('opts==x')
        //   // console.log(`param:${param}=|${result}|`)
        //   return `param:${param}=|${result}|`
        // }

        // UNMASKED_VENDOR_WEBGL
        if (param === 37445) {
          // console.log('opts==XXX')
          // console.log(opts)
          // console.log(param)

          return opts.vendor || 'Intel Inc.' // default in headless: Google Inc.
        }
        // UNMASKED_RENDERER_WEBGL
        if (param === 37446) {
          // console.log('opts==XXX')
          // console.log(opts)
          // console.log(param)

          return opts.renderer || 'Intel Iris OpenGL Engine' // default in headless: Google SwiftShader
        }
        return result
      }
    }

    // There's more than one WebGL rendering context
    // https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext#Browser_compatibility
    // To find out the original values here: Object.getOwnPropertyDescriptors(WebGLRenderingContext.prototype.getParameter)
    const addProxy = (obj, propName) => {
      utils.replaceWithProxy(obj, propName, getParameterProxyHandler)
    }
    // For whatever weird reason loops don't play nice with Object.defineProperty, here's the next best thing:
    addProxy(WebGLRenderingContext.prototype, 'getParameter')
    addProxy(WebGL2RenderingContext.prototype, 'getParameter')
  } catch (err) {
    console.log("====err");
    console.warn(err);
  }
}