# alwaysdata Demo: Server-Sent Events Broadcast

This project aims at demonstrating how to build and architect a micro-services application, using a broadcasting Pub/Sub system, and pushing content to a frontend page in real-time.

As a demo built by the [alwaysdata](https://www.alwaysdata.com) team, this readme is opinionated to a deployment on the _alwaysdata_ PaaS provider, but those instructions can be used by any other hosting solutions.

## Pre-requisites

1. Make sure you [use a Python 3 version](https://help.alwaysdata.com/en/languages/python/configuration/#environment) in your environment
2. Create a venv in your server account for our different parts:
   ```sh
   $ python -m venv ~/.local/share/venvs/default
   ```

## Packages

This project uses 4 different packages as parts of our application:

- the _broadcaster_: a simple [Flask](https://flask.palletsprojects.com/en/2.3.x/) app allowing to display of a single page and handles `POST` from it, broadcasting then messages to the app.
- the _forwarder_: a [ØMQ](https://zeromq.org/) Python app that acts like a broker, handling messages from broadcasters and relaying them to other parts
- the _logger_: a static HTML page handling a stream that rely on [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) browsers' capabilities to update its content in real-time
- the _streamer_: a [Deno app](https://examples.deno.land/http-server-streaming) listening for messages from the common channel and building a stream ready to be read by an SSE-compatible page

## How it works

This app has two different frontends:

- one served by the _broadcaster_
- the _logger_

When you open the _logger_ the page is first empty. It opens a socket to the stream emitted by the _streamer_, and waits for updates.

When a user opens the main page served by the _broadcaster_ and starts interacting with it, actions are `POST` to its backend (like any tracking solution). For each `POST` request, the _broadcaster_ backend emits on the common channel, implemented by the _forwarder_ in a Pub/Sub pattern.

The streamer, when launched, listens to the messages from the common channel and filters and formats them in a stream ready to be handled by a webpage implementing the _Server-Sent Events_ protocol.

When you open the _logger_ page, it opens a socket to the stream from the _streamer_ and live-updates its content accordingly.

## Deployment at alwaysdata

In your [account on SSH](https://help.alwaysdata.com/en/remote-access/ssh/) server, clone this repository:

```sh
$ git clone https://github.com/alwaysdata/ad-demo-sse.git ~/sse
```

The `<account>` string must be replaced by your account name.
The `<base_url>` string is your alwaysdata's default URL in the shape of `<account>.alwaysdata.net`.


### Forwarder

Create a new [Service](https://help.alwaysdata.com/en/services/).

- command: `/home/<account>/.local/share/venvs/default/bin/python main.py`
- working directory: `/home/<account>/sse/packages/forwarder/`
- environment:
  ```
  XSUB_PORT=8300
  XPUB_PORT=8301
  IP=[::]
  ````

### Streamer

Create a new [Site](https://help.alwaysdata.com/en/sites/) of type `Deno`.

- address: `<base_url>/events`
- command: `deno run --allow-net --allow-env index.ts`
- working directory: `/home/<account>/sse/packages/streamer/`
- environment:
  ```
  ZMQ_PORT=8301
  ZMQ_HOST=services-<account>.alwaysdata.net
  ```

### Logger

Create a new [Site](https://help.alwaysdata.com/en/sites/) of type `Static files`.

- address: `<base_url>/logger/`
- root directory: `/sse/packages/logger/`

### Broadcaster

Create a new [Site](https://help.alwaysdata.com/en/sites/) of type `Python WSGI`.

- address: `<base_url>`
- application path: `main:app`
- working directory: `/sse/packages/broadcaster/`
- environment:
  ```
  ZMQ_PORT=8300
  ZMQ_HOST=services-<account>.alwaysdata.net
  ````
- virtualenv directory: `/.local/share/venvs/default/`


## Going further...

For more information and motivations about this demo, have a look at [Chasing the White Rabbit: a micro-services-oriented WebApp with broadcasted Server Sent Events](https://blog.alwaysdata.com/2023/06/23/chasing-the-white-rabbit-a-micro-services-oriented-webapp-with-broadcasted-server-sent-events/), an article at alwaysdata's blog.

## Authors

- Mads - m4dz@alwaysdata.com