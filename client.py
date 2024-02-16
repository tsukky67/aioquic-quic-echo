# client.py
import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration

async def run_client(host, port, ca_cert_path):
    configuration = QuicConfiguration(is_client=True)
    configuration.load_verify_locations(cafile=ca_cert_path)

    async with connect(host, port, configuration=configuration) as protocol:
        print("Connecting to server...",end="")
        await protocol.wait_connected()
        reader, writer = await protocol.create_stream()
        print("Connected")

        while not reader.at_eof():
            text = input("Message: ")
            writer.write((text).encode())
            print("Sending to server...",end="")
            await reader.read(1024)

        print("done")
        print("Sending eof...",end="")
        writer.write_eof()
        protocol.close()
        await protocol.wait_closed()
        print("done")

def main():
    asyncio.run(run_client('localhost', 4433, 'ca_cert.pem'))

if __name__ == "__main__":
    main()
