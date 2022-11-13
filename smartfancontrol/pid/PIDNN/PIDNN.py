from smartfancontrol.pid.PIDNN.Neuron import Neuron
from simple_pid import PID as SimplePID
import numpy as np

"""
A PIDNN implementation
"""
class PIDNN:

    def transfer_X(self, x, i, o, *args):
        return x

    def transfer_P(self, x, i, o, *args):
        if x > 1: return 1
        if x < -1: return -1
        return x

    def transfer_I(self, x, i, o, *args):
        if x > 1: return 1
        if x < -1: return -1
        return x + i[1]

    def transfer_D(self, x, i, o, *args):
        if x > 1: return 1
        if x < -1: return -1
        return x - i[1]

    def transfer_ouput(self, x, i, o, *args):
        p, i, d = x
        self.pid.Kp = p
        self.pid.Ki = i
        self.pid.Kd = d
        return self.pid(args[0])

    def __init__(self, memory, dt, setpoint, initial_gains=[-2.854, -0.021, -0.389]):
        self.setpoint = setpoint
        self.dt = dt
        self.memory = memory
        p, i, d = initial_gains
        self.pid = SimplePID(p, i, d, setpoint=50, output_limits=(0, 100))
        self.pid_history = [initial_gains]
        self.error_log = []
        self.feedback = [0 for _ in range(memory)]
        self.input_layer = [
            Neuron(memory, self.transfer_X),
            Neuron(memory, self.transfer_X)
        ]

        self.input_weights = [[2.7834375, 0.7602471875000001], [1.5240624999999999, -0.5616021874999999],
                              [0.5297779921874999, -1.411404864921875]]
        # [[1.0, -1.0], [1.0, -1.0], [1.0, -1.0]]
        # [[2.7834375, 0.7602471875000001], [1.5240624999999999, -0.5616021874999999], [0.5297779921874999, -1.411404864921875]]
        # [[2.4348125000000005, 0.40611624999999996], [1.0583405971294575, -0.9445144329703188], [1.19575, -0.808165]]

        self.hidden_layer = [
            Neuron(memory, self.transfer_P),
            Neuron(memory, self.transfer_I),
            Neuron(memory, self.transfer_D),
        ]

        self.hidden_weights = [
            [-3.2071250000000013, -0.15289919112197042, -0.7289999999999991]]  # [[-2.854, 0.021, -0.389]]

        self.output_layer = [Neuron(memory, self.transfer_ouput)]

    def error(self):
        return self.setpoint - self.feedback[0]

    def act(self):
        self.input_layer[0].act(self.setpoint)
        self.input_layer[1].act(self.feedback[0])

        self.error_log.append(self.error())

        for i in range(len(self.hidden_layer)):
            input = 0
            for j in range(len(self.input_layer)):
                input += self.input_layer[j].output[0] * self.input_weights[i][j]

            self.hidden_layer[i].act(input)

        for i in range(len(self.output_layer)):
            pid_gains = [self.hidden_layer[j].output[0] * self.hidden_weights[i][j] for j in
                         range(len(self.hidden_layer))]
            self.pid_history.append(pid_gains)
            self.output_layer[i].act(pid_gains, self.feedback[0])

        return self.output_layer[0].output[0]

    def update_feedback(self, v):
        self.feedback.insert(0, v)
        self.feedback.pop()

    def train(self):
        error = abs(self.error())

        threshold = self.setpoint * 0.02
        if threshold >= error:
            return

        m = self.memory - 1
        dz = lambda x: 0 if x == 0 else 1 / x
        sign = np.sign

        for i in range(len(self.hidden_layer)):
            delta = 0;

            for k in range(m):
                delta += (self.input_layer[0].input[k] - self.input_layer[1].input[k]) \
                         * sign((self.feedback[k] - self.feedback[k + 1]) \
                                * dz(self.output_layer[0].output[k] - self.output_layer[0].output[k + 1])) \
                         * self.hidden_layer[i].output[k]

            delta *= -1 / m;

            self.hidden_weights[0][i] -= self.dt * delta;

        for i in range(len(self.hidden_layer)):
            for j in range(len(self.input_layer)):
                delta = 0;

                for k in range(m):
                    delta += \
                        (self.input_layer[0].input[k] - self.input_layer[1].input[k]) \
                        * sign((self.feedback[k] - self.feedback[k + 1]) \
                               * dz(self.output_layer[0].output[k] - self.output_layer[0].output[k + 1])) \
                        * self.hidden_weights[0][i] \
                        * sign(
                            (self.hidden_layer[i].output[k] - self.hidden_layer[i].output[k + 1])
                            * dz(self.hidden_layer[i].input[k] - self.hidden_layer[i].input[k + 1])
                        ) \
                        * self.input_layer[j].output[k]

                delta *= (-2 / m)

                self.input_weights[i][j] -= self.dt * delta
