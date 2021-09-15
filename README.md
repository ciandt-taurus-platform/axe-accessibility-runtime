# AXE Accessibility Test Runtime

This repo utilizes the core funcionatility provided by [Deque/Axe](https://github.com/dequelabs/axe-core) to execute accessibility tests.

It's using the Puppeteer under the hood to create a ChromeDriver instance and run the provided url against a set of rules. More about it [here](https://github.com/dequelabs/axe-core/tree/develop/doc/examples/puppeteer)

You can incorporate it into your CI/CD pipeline or you can call it as part of you testing framework.

(JPM Plugin is a possible future improvement)

## Table of Contents  

<!--ts-->
- [Getting-started With the Runtime](#getting-started-with-the-runtime)
- [Support Execution Scripts](#support-execution-scripts)
  - [Running a batch test against a list of urls](#running-a-batch-test-against-a-list-of-urls)
  - [Running it using Jenkinsfile](#running-it-using-a-jenkinsfile)

<!--te-->

# Getting-started With the Runtime

## Running axe locally

**Requirements:**

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

```javascript
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
    }
  ]
  ...
}

```

# Execution Scripts

Even though it's possible to manually execute the scan (as described in the setions above), it's limited to one url per execution. To be able to scan an entire website with **n** pages, one would need to manually run it **n** times.

To make things more smoothly, there is one folder named **"exec_scripts"** containing some supporting python, bash and jenkins scripts to facilitate the execution and the results aggregation and manipulation.

## Running a batch test against a list of urls

It's possible to execute a batch test and consolidate the results using the **exec_from_file_list.py**. It uses a text file containg a list of urls and iterate over each one of it consolidating the results in a key-value structure url -> result.

```bash
python3 exec_from_file_list.py -f <inputfile> -i <scanner_docker_image_name>
```

*Example*:
```bash
python3 exec_from_file_list.py -f tesdata/urls.txt -i axe-accessibility-runtime
```

Results example:

```javascript
{
  "https://www.hubspot.com/products/operations/programmable-automation\n": {
    "testEngine": {
      "name": "axe-core",
      "version": "3.5.6"
    },
    "testRunner": {
      "name": "axe"
    },
    "testEnvironment": {
      "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/78.0.3882.0 Safari/537.36",
      "windowWidth": 800,
      "windowHeight": 600,
      "orientationAngle": 0,
      "orientationType": "portrait-primary"
    },
    "timestamp": "2021-09-15T14:18:02.876Z",
    "url": "https://www.hubspot.com/products/operations/programmable-automation",
    "toolOptions": {
      "reporter": "v1"
    },
    "violations": [
      {
        "id": "aria-hidden-focus",
        "impact": "serious",
        "tags": [
          "cat.name-role-value",
          "wcag2a",
          "wcag412",
          "wcag131"
        ],
        "description": "Ensures aria-hidden elements do not contain focusable elements",
        "help": "ARIA hidden element must not contain focusable elements",
        "helpUrl": "https://dequeuniversity.com/rules/axe/3.5/aria-hidden-focus?application=axeAPI",
        "nodes": [
          {
            "any": [],


```


## Running it using a jenkinsfile

Concatenating the python in a Jenkinsfile allows the execution as a pipeline step.
It's mandatory the Jenkins executor has access to a docker client in the $PATH. To overcome this requirement it's possible to use the Docker jenkins plugin.

```groovy

node {
    git branch: "main", 
        url: 'https://${ACCESS_KEY}@github.com/ciandt-taurus-platform/axe-accessibility-runtime'
   
    sh("pip install -r exec_scripts/requirements.txt")
    sh("python3 exec_scripts/exec_from_file_list.py -f urls.txt -i axe-accessibility-runtime")
}

```