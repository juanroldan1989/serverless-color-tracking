# serverless-color-tracking

[Serverless Framework] :robot: Live Events Tracking :vertical_traffic_light: Clicks &amp; Hovers on Colors :dart: Dashboards

# Core Features

- Create **events** based on user's actions (`/v1/events` endpoint):

```ruby
$ curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"action_color": { "action_name" : "hover", "color_name" : "red" } }' \
  https://<api-id>.execute-api.<region>.amazonaws.com/dev/v1/events

> {"message": "Message placed in serverless-color-tracking-dev-hoversStream successfully."}%
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
