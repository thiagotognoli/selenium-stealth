platform => {
  // Overwrite the `vendor` property to use a custom getter.
  Object.defineProperty(Object.getPrototypeOf(navigator), 'platform', {
    get: () => platform || 'Win64'
  })
}
