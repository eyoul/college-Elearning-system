import Pyro4
import threading
import signal
import sys
from elearning import create_app

daemon = None  # Global reference to the Pyro4 daemon

@Pyro4.expose
class Hello(object):
    def sayHello(self):
        print("Hello, World!")
        return "Hello, World!"

def run_server():
    global daemon
    daemon = Pyro4.Daemon()
    uri = daemon.register(Hello)
    print("Server Ready. URI:", uri)
    with open("server_uri.txt", "w") as f:
        f.write(str(uri))
    daemon.requestLoop()

def run_app():
    app = create_app()
    app.run(debug=True, use_reloader=False, threaded=True)

def signal_handler(sig, frame):
    print('Shutting down...')
    if daemon:
        daemon.shutdown()  # Properly shutdown the Pyro4 daemon
    # For Flask, there's no built-in shutdown mechanism when running with app.run()
    # In a production environment, use a WSGI server that can be programmatically shutdown
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # Setup signal handler

    # Run the Pyro4 server in a separate thread, making it a daemon thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run the Flask app in a separate thread, also as a daemon thread
    app_thread = threading.Thread(target=run_app, daemon=True)
    app_thread.start()
    
    # Main thread now waits for the signal interrupt
    server_thread.join()
    app_thread.join()
