# alwaysdata Demo: Server Sent Events Broadcast

This project aims at demonstrating how to build and architect a micro-services application, using a broadcasting Pub/Sub system, and pushing content to a frontend page in real-time.

As a demo built by the [alwaysdata](https://www.alwaysdata.com) team, this readme is opinionated to a deployment on the _alwaysdata_ PaaS provider, but those instructions can be used by any other hosting solutions.

## Pre-requisites

1. Make sure you use a Python 3 version in your environment
2. Create a venv in your server account for our different parts:
   ```sh
   $ python -m venv ~/.local/share/venvs/default
   ```

## Packages

This project uses 4 different packages as parts of our application:

- the _broadcaster_: a simple Flask app allowing to display of a single page and handles `POST` from it, broadcasting then messages to the app.
- the _forwarder_: a ØMQ python app that acts like a broker, handling messages from broadcasters and relaying them to other parts
- the _logger_: a static HTML page handling a stream that to _Server Sent Events_ browsers' capabilities to update its content in real-time
- the _streamer_: a Deno app listening for messages from the common channel and building a stream ready to be read by an SSE-compatible page

## How it works

This app has two different frontends:

- one served by the _broadcaster_
- the _logger_

When you open the _logger_ the page is first empty. It opens a socket to the stream emitted by the _streamer_, and waits for updates.

When a user opens the main page served by the _broadcaster_ and starts interacting with it, actions are `POST` to its backend (like any tracking solution). For each `POST` request, the _broadcaster_ backend emits on the common channel, implemented by the _forwarder_ in a Pub/Sub pattern.

The streamer, when launched, listens to the messages from the common channel and filters and formats them in a stream ready to be handled by a webpage implementing the _Server Sent Events_ protocol.

When you open the _logger_ page, it opens a socket to the stream from the _streamer_ and live-updates its content accordingly.

## Deployment at alwaysdata

[TBD]

## Going further...

For more information and motivations about this demo, have a look at [this article]() at the alwaysdata's blog.

## Authors

- Mads - m4dz@alwaysdata.com