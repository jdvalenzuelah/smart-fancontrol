class Neuron:

    def __init__(self, memory, transfer_func):
        self.input = [0 for _ in range(memory)]
        self.output = [0 for _ in range(memory)]
        self.transfer_func = transfer_func

    def act(self, new_input, *args):
        new_output = self.transfer_func(new_input, self.input, self.output, *args)

        self.input.insert(0, new_input)
        self.input.pop()

        self.output.insert(0, new_output)
        self.output.pop()

        return new_output
