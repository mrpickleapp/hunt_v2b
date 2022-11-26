import net

class AI():

    def __init__(self, n):
        self.network = net.Network()
        self.network.add(net.FCLayer(n, n))
        self.network.add(net.ActivationLayer(net.relu, net.relu))
        self.network.add(net.FCLayer(n, 3))
        self.network.add(net.ActivationLayer(net.direct, net.direct))

    def compute(self, input):
        out = self.network.predict(input)
        return out

    def evolve(self, evolution_rate):
        self.network.evolve(evolution_rate=evolution_rate)