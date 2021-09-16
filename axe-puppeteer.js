const puppeteer = require('puppeteer');
const axeCore = require('axe-core');
const { parse: parseURL } = require('url');
const assert = require('assert');
const argParse = require("minimist")

// Cheap URL validation
const isValidURL = input => {
  const u = parseURL(input);
  return u.protocol && u.host;
};

const parseHeaders = input => {
    if(typeof input === "undefined") {
      return {};
    }

    //parse single header
    if(typeof input === "string") {
      return parseHeader(input)
    }

    //parse array
    var merged = {};
    input.map(parseHeader).forEach(element => {
      for (var attrname in element) { merged[attrname] = element[attrname]; }
    });
    
    return merged

};

const parseHeader = header => {
  obj = {}

  contents = header.split(":")
  obj[contents[0]] = contents[1]

  return obj
}

args = argParse(process.argv.slice(2))
url = args["_"][0]
assert(isValidURL(url), 'Invalid URL');

headers = parseHeaders(args["H"])

const main = async (url, headers) => {
  let browser;
  let results;
  try {
    // Setup Puppeteer
    browser = await puppeteer.launch({
      args: ['--no-sandbox']
    });

    // Get new page
    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(0);
    await page.setExtraHTTPHeaders(headers)
    await page.goto(url);

    // Inject and run axe-core
    const handle = await page.evaluateHandle(`
			// Inject axe source code
			${axeCore.source}
			// Run axe
			axe.run()
		`);

    // Get the results from `axe.run()`.
    results = await handle.jsonValue();
    // Destroy the handle & return axe results.
    await handle.dispose();
  } catch (err) {
    // Ensure we close the puppeteer connection when possible
    if (browser) {
      await browser.close();
    }

    // Re-throw
    throw err;
  }

  await browser.close();
  return results;
};

main(url, headers)
  .then(results => {
    console.log(JSON.stringify(results));
  })
  .catch(err => {
    console.error('Error running axe-core:', err.message);
    process.exit(1);
  });