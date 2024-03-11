<img src="https://github.com/juanroldan1989/color-tracking/blob/main/color-tracking-header.png" alt="juanroldan1989 color-tracking">

<h4 align="center">Events Tracking Platform 🚦 Clicks & Hovers on Colors 🎯 Live Graphs & Counters</h4>

<p align="center">
  <a href="https://github.com/juanroldan1989/serverless-color-tracking/commits/master">
  <img src="https://img.shields.io/github/last-commit/juanroldan1989/serverless-color-tracking.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub last commit">
  <a href="https://github.com/juanroldan1989/serverless-color-tracking/issues">
  <img src="https://img.shields.io/github/issues-raw/juanroldan1989/serverless-color-tracking.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub issues">
  <a href="https://github.com/juanroldan1989/serverless-color-tracking/pulls">
  <img src="https://img.shields.io/github/issues-pr-raw/juanroldan1989/serverless-color-tracking.svg?style=flat-square&logo=github&logoColor=white" alt="GitHub pull requests">
  <a href="https://github.com/juanroldan1989/serverless-color-tracking/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg">
  </a>
  <a href="https://twitter.com/intent/tweet?text=Hey%20I've%20just%20discovered%20this%20cool%20app%20on%20Github%20by%20@JhonnyDaNiro%20-%20Color%20Tracking%20Live%20Events%20With%20Dashboards&url=https://github.com/juanroldan1989/serverless-color-tracking/&via=Github">
  <img src="https://img.shields.io/twitter/url/https/github.com/juanroldan1989/serverless-color-tracking.svg?style=flat-square&logo=twitter" alt="GitHub tweet">
</p>

# Core Features

<div align="left">
  <img width="800" src="https://github.com/juanroldan1989/color-tracking/blob/main/color-tracking-live-demo.gif" />
</div>

- Create **events** based on user's actions (`/v1/events` endpoint):

```ruby
$ curl -X POST \
  -H "Content-Type: application/json" \
  -H "x-api-key: <api-key>" \
  -d '{"action_color": { "action_name" : "hover", "color_name" : "red" } }' \
  https://<api-id>.execute-api.<region>.amazonaws.com/dev/v1/events

> {"message": "Message placed in serverless-color-tracking-dev-hoversStream successfully."}%
```

- Get **stats** filtered by `action` value via "polling" implementation through REST API endpoint available:

```ruby
$ curl -H "Content-Type: application/json" \
  -H "x-api-key: <api-key>" \
  https://<api-id>.execute-api.<region>.amazonaws.com/dev/v1/stats?action=click
```

- Get **stats** via websockets. This way the API can push updates across clients:

```ruby
$(document).ready(function() {
  var socket;

  // Connect websockets
  socket = new ReconnectingWebSocket("wss://<api-id>.execute-api.<region>.amazonaws.com/dev");

  socket.onopen = function(event) {
    data = {"action": "live", "api_key" : "XXXXXX", "event_type": "click"};
    // data = {"action": "live", "api_key" : "XXXXXX", "event_type": "hover"};
    socket.send(JSON.stringify(data));
  };

  // Setup listener for messages
  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    // drawDashboard(data, "hovers");
    drawDashboard(data, "clicks");
  };
});
```

<img src="https://github.com/juanroldan1989/serverless-color-tracking/raw/main/screenshots/system-design.png" width="100%" />

## Deployment

````ruby
$ sls deploy

Deploying serverless-color-tracking to stage dev (region)

✔ Service deployed to stack serverless-color-tracking-dev (41s)

endpoint: POST - https://<api-id>.execute-api.<region>.amazonaws.com/dev/v1/events
functions:
  createEvent: serverless-color-tracking-dev-createEvent (2.5 kB)
  clicksConsumer: serverless-color-tracking-dev-clicksConsumer (2.5 kB)
  hoversConsumer: serverless-color-tracking-dev-hoversConsumer (2.5 kB)
```

1 function at a time:

```ruby
$ sls deploy function --function createEvent
````

## Bundling dependencies

In case you would like to include third-party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).

## Deep Dive DynamoDB queries

https://staskoltsov.medium.com/deep-dive-into-query-and-filter-operations-in-dynamodb-ccfe4ef24e02

https://dynobase.dev/dynamodb-filterexpression/

## CORS with Serverless

https://www.serverless.com/blog/cors-api-gateway-survival-guide

## AWS Websockets

https://docs.amazonaws.cn/en_us/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-wscat.html

https://ably.com/blog/how-to-build-a-serverless-websocket-platform

10 Realtime Data sources: https://ably.com/blog/10-realtime-data-sources-you-wont-believe-are-free

https://levelup.gitconnected.com/creating-a-chat-app-with-serverless-websockets-and-python-a-tutorial-54cbc432e4f

Testing:

```ruby
$ npm install -g wscat
```

Connect to your endpoint using the wss:// url from your deploy output:

```ruby
wscat -c <YOUR_WEBSOCKET_ENDPOINT>
connected (press CTRL+C to quit)
>
```

Send a message. Note that the action key in the message is used for the route selection, all other keys can be changed to your liking:

```ruby
> {"action": "live", "api_key": "api_key", "event_type": "click"}
> {"action": "live", "api_key": "api_key", "event_type": "hover"}
```
