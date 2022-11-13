from smartfancontrol.server.IPMIToolSSH import IPMIToolSSH
from smartfancontrol.server.ipmi.DellIDRAC6 import DellIDRAC6
from smartfancontrol.server.linux.LinuxSensors import LinuxSensors
from smartfancontrol.pid.PIDNN.PIDNNFanSpeedCurve import PIDNNFanSpeedCurve
from smartfancontrol.pid.PIDNN.PIDNN import PIDNN
from sfc.ControlLoop import ControlLoop
from simple_pid import PID
from smartfancontrol.pid.PIDFanSpeedCurve import PIDFanSpeedCurve

if __name__ == '__main__':
    server = IPMIToolSSH(
        host='',
        port=22,
        username='',
        password="",
        commands=DellIDRAC6(),
        tempsensor=LinuxSensors()
    )

    server.execCmd('stress -c 4 -m 8 -t 3000s')

    fanprofile = PIDNNFanSpeedCurve(PIDNN(2, 0.05, 50))
    #fanprofile = PIDFanSpeedCurve(PID(-2.854, -0.021, -0.389, setpoint=50, output_limits=(0, 100)))

    inter = 0

    def hook(**kwargs):
        print(kwargs)
        with open('data.csv', 'a') as f:
            feedback = kwargs["feedback"]
            time = kwargs["time"]
            speed = kwargs['newState']
            f.write(f'{feedback},{time},{speed}\n')

    control = ControlLoop(server, fanprofile, cycleHook=hook)

    control.start()




