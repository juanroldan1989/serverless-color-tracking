# serverless-color-tracking

[Serverless Framework] :robot: Live Events Tracking :vertical_traffic_light: Clicks &amp; Hovers on Colors :dart: Dashboards

# Core Features

- Create **events** based on user's actions (`/v1/events` endpoint):

```ruby
$ curl -X POST \
  -H "Content-Type: application/json" \
  -H "x-api-key: <api-key>" \
  -d '{"action_color": { "action_name" : "hover", "color_name" : "red" } }' \
  https://<api-id>.execute-api.<region>.amazonaws.com/dev/v1/events

> {"message": "Message placed in serverless-color-tracking-dev-hoversStream successfully."}%
```

- Get **stats** filtered by `action` value:

```ruby
$ curl -H "Content-Type: application/json" \
  -H "x-api-key: <api-key>" \
  https://<api-id>.execute-api.<region>.amazonaws.com/dev/v1/stats?action=click
```

- Websockets connection available. This way the API can push updates across clients:

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
    // drawChart(data, "hovers");
    drawChart(data, "clicks");
  };
});
```

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
