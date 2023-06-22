import os

import zmq

XSUB_PORT = os.environ.get("XSUB_PORT", 5556)
XPUB_PORT = os.environ.get("XPUB_PORT", 5555)
HOST = os.environ.get("IP", "0.0.0.0")

xsub_url = f"tcp://{HOST}:{XSUB_PORT}"
xpub_url = f"ws://{HOST}:{XPUB_PORT}"


def _main():
    ctx = zmq.Context(1)

    sub = ctx.socket(zmq.SUB)
    pub = ctx.socket(zmq.PUB)

    try:
        # Socket facing clients
        sub.setsockopt(zmq.IPV6, 1)
        sub.bind(xsub_url)
        sub.setsockopt(zmq.SUBSCRIBE, b"")
        print(f"Forwarder ready to receive on {xsub_url}")

        # Socket facing services
        pub.setsockopt(zmq.IPV6, 1)
        pub.bind(xpub_url)
        print(f"Forwarder ready to send on {xpub_url}")

        zmq.proxy(sub, pub)

    except (KeyboardInterrupt, Exception) as e:
        print(e)
        print("Bringing down zmq forwarder")

    finally:
        sub.close()
        pub.close()
        ctx.term()


if __name__ == "__main__":
    _main()
