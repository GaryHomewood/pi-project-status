# Pi project status

## Overview

A simple web client and python Flask API to be run on a Rasperry Pi with an LED shim, for traffic lighting the status of a project.

## Dependencies

```bash
brew install yarn
yarn global add parcel-bundler
```

## API

```bash
workon env-name
export FLASK_APP=main.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 # so it's visible from other devices on the same network via IP address
```

## Web

.env variables

```bash
API_SERVER=ip address
API_PORT=port number
```

Use data from `project-data.json` to generate the html.

```bash
yarn run build
```

Start up a developement server, including auto rebuild on file changes:

```bash
parcel index.html
```

Build and minimise assets to the `dist` folder:

```bash
parcel build index.html
```
