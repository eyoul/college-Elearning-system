
import Pyro4

try:
    # Read the URI from the file
    with open("server_uri.txt", "r") as f:
        uri = f.read().strip()

    # Connect to the Pyro4 server
    hello = Pyro4.Proxy(uri)

    # Call the sayHello method
    response = hello.sayHello()
    print("Response:", response)

    # Run something after receiving the response
    print("Access using http://127.0.0.1:5000/ address ")

except Exception as e:
    print("Client exception:", str(e))

