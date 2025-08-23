
import socket
import json

def check_kodi_connection(host='127.0.0.1', port=9090, timeout=10):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            print(f"Successfully connected to Kodi on {host}:{port}")
            
            # Optional: Send a simple JSON-RPC request to verify communication
            request = {
                "jsonrpc": "2.0",
                "method": "JSONRPC.Ping",
                "id": 1
            }
            
            with socket.create_connection((host, port), timeout=timeout) as s:
                s.sendall(json.dumps(request).encode('utf-8') + b'\r\n')
                response = s.recv(1024)
                if response:
                    response_data = json.loads(response)
                    if response_data.get("result") == "pong":
                        print("Successfully received pong from Kodi")
                        return True
                    else:
                        print(f"Received unexpected response from Kodi: {response_data}")
                        return False
                else:
                    print("No response from Kodi")
                    return False

    except socket.error as err:
        print(f"Failed to connect to Kodi: {err}")
        return False

if __name__ == "__main__":
    if not check_kodi_connection():
        exit(1)
