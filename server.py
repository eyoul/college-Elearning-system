import Pyro4

@Pyro4.expose
class Hello(object):
    def sayHello(self):
        return "Hello, World!"

daemon = Pyro4.Daemon()
uri = daemon.register(Hello)

# Print the dynamically generated URI
print("Server Ready. URI:", uri)

# Save the URI to a file so that the client can read it
with open("server_uri.txt", "w") as f:
    f.write(str(uri))

daemon.requestLoop()
"""
import Pyro4
from app import run_app

@Pyro4.expose
class Hello(object):
    def sayHello(self):
        print("Hello, World!")
        # Run app.py after printing "Hello, World!"
        run_app()
        return "Hello, World!"

daemon = Pyro4.Daemon()
uri = daemon.register(Hello)

print("Server Ready. URI:", uri)
with open("server_uri.txt", "w") as f:
    f.write(str(uri))

daemon.requestLoop()
"""
