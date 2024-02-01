
import Pyro4
import subprocess

try:
    # Read the URI from the file
    with open("server_uri.txt", "r") as f:
        uri = f.read().strip()

    hello = Pyro4.Proxy(uri)
    response = hello.sayHello()
    print("Response:", response)

    # Run app.py after receiving the response
    subprocess.Popen(["python", "app.py"])

except Exception as e:
    print("Client exception:", str(e))


"""

# to access the Hello World 
import Pyro4

try:
    # Read the URI from the file
    with open("server_uri.txt", "r") as f:
        uri = f.read().strip()

    hello = Pyro4.Proxy(uri)
    response = hello.sayHello()
    print("Response:", response)
except Exception as e:
    print("Client exception:", str(e))

"""