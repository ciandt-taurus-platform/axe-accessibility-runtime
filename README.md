# AXE Accessibility Test Runtime

This repo utilizes the core funcionatility provided by [Deque/Axe](https://github.com/dequelabs/axe-core) to execute accessibility tests.

It's using the Puppeteer under the hood to create a ChromeDriver instance and run the provided url against a set of rules. More about it [here](https://github.com/dequelabs/axe-core/tree/develop/doc/examples/puppeteer)

You can incorporate it into your CI/CD pipeline or you can call it as part of you testing framework.

(JPM Plugin is a possible future improvement)


# Getting-started

## Running axe locally

Requirements:

Node v8+ in PATH


1. Download the dependencies

```bash
npm install
```

2. Execute the test using *node axe-puppeteer.js {url}*

```bash
node axe-puppeteer.js https://ciandt.com
```

## Runnning on docker

1. Build the docker image

```bash
docker build . -t axe-accessibility-runtime
```

2. Execute the docker image passing the url as a parameter

```bash
docker run --rm axe-accessibility-runtime https://ciandt.com
```


# How to interpret the results

The most important result segment is the "violations" field array. It shows if any tag or html element is violating any accessbility best-practices.

```json
{
  testEngine: { name: 'axe-core', version: '3.5.6' },
  testRunner: { name: 'axe' },
  testEnvironment: {
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/78.0.3882.0 Safari/537.36',
    windowWidth: 800,
    windowHeight: 600,
    orientationAngle: 0,
    orientationType: 'portrait-primary'
  },
  timestamp: '2021-09-13T15:14:11.367Z',
  url: 'https://ciandt.com/br/',
  toolOptions: { reporter: 'v1' },
  violations: [   <========================== ISSUES HERE
    {
      id: 'duplicate-id',
      impact: 'minor',
      tags: [Array],
      description: 'Ensures every id attribute value is unique',
      help: 'id attribute value must be unique',
      helpUrl: 'https://dequeuniversity.com/rules/axe/3.5/duplicate-id?application=axeAPI',
      nodes: [Array]
    },
    {
      id: 'frame-title',
      impact: 'serious',
      tags: [Array],
      description: 'Ensures <iframe> and <frame> elements contain a non-empty title attribute',
      help: 'Frames must have title attribute',
      helpUrl: 'https://dequeuniversity.com/rules/axe/3.5/frame-title?application=axeAPI',
      nodes: [Array]
    },
    {

```