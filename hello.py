import Pyro4

@Pyro4.expose
class Hello(object):
    def sayHello(self):
        return "Hello, World!"
