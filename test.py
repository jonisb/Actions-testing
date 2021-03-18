from multiprocessing import Process, Queue

# must be a global function
def my_function():
    import http.server
    import socketserver

    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


if __name__ == '__main__':
    p = Process(target=my_function)
    p.start()

    import time
    import urllib.request

    time.sleep(10)

    with urllib.request.urlopen('http://localhost:8000') as f:
        print(f.read(300))

    p.terminate()