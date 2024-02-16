# server.py
import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

async def handle_stream(reader, writer):
    print("New stream opened.")
    data = await reader.read(1024)
    while not reader.at_eof():
        print(f"Received: {data.decode()}")
        writer.write_eof()
        data = await reader.read(1024)
    print("Stream closed.")

async def run_server(host, port):
    configuration = QuicConfiguration(is_client=False)

    configuration.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    def handle_stream_awaited(reader, writer):
        asyncio.create_task(handle_stream(reader, writer))
    await serve(host, port, configuration=configuration, stream_handler=handle_stream_awaited)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server('localhost', 4433))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

if __name__ == "__main__":
    main()
