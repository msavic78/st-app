import requests
import websockets
import asyncio

async def test_connection():
    try:
        # Step 1: Test HTTPS connection to proxy
        response = requests.get('https://www.roomsync.roomhandler.com', timeout=5)
        if response.status_code == 200:
            print("HTTPS connection to proxy successful.")
        else:
            print("HTTPS connection to proxy failed.")
            return

        # Step 2: Attempt WebSocket upgrade to roomsync endpoint
        async with websockets.connect('wss://roomsync.roomhandler.com/_stcore/stream') as websocket:
            print("WebSocket connection established.")

            # You can add logic to send/receive test messages here 
            # Example:
            # await websocket.send("Test message")
            # response = await websocket.recv()
            # print(f"Received: {response}")

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to proxy: {e}")
    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())