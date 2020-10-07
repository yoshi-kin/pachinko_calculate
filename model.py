from machines import kamen

class User(object):
    machine = []
    count = []
    rate = []
    def __init__(self, id=None):
        self.id = id

    def push_machine(self, data):
        self.__class__.machine.append(data)

    def push_count(self, data):
        self.__class__.count.append(data)

    def push_rate(self, data):
        self.__class__.rate.append(data)

    def calculate(self, func=None):
        expected_value = func(int(self.count[-1]), float(self.rate[-1]))
        rounded_value = round(expected_value)
        return rounded_value




