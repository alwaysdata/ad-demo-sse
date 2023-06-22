import { serve } from "https://deno.land/std@0.184.0/http/server.ts";

import { Sub } from "https://deno.land/x/jszmq/mod.ts";


const port: number | undefined = Deno.env.get("PORT");
const hostname: string | undefined = Deno.env.get("IP");

const zmq_port: string = Deno.env.get("ZMQ_PORT")
const zmq_hostname: string = Deno.env.get("ZMQ_HOST")


function handler(_req: Request): Response {

	const sock = new Sub();
	sock.connect(`ws://${zmq_hostname}:${zmq_port}`);
	sock.subscribe("");

  const body = new ReadableStream({

    start(controller) {
			sock.on("message", function (endpoint, raw_data) {
				const {event, level, message, urgent} = JSON.parse(raw_data,toString());
				let data = {message, level}
				if (urgent) {
					data['notify'] = true;
				}
				
				let msg = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
        controller.enqueue(new TextEncoder().encode(msg));
			});
    },

    cancel() {
			sock.close()
    },
  });

  return new Response(body, {
    headers: {
      "content-type": "text/event-stream",
      "x-content-type-options": "nosniff",
			"cache-control": "no-store",
			"access-control-allow-origin": "*",
    },
  });
}

serve(handler, {port, hostname});