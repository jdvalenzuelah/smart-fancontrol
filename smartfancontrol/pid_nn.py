from smartfancontrol.server.IPMIToolSSH import IPMIToolSSH
from smartfancontrol.server.ipmi.DellIDRAC6 import DellIDRAC6
from smartfancontrol.server.linux.LinuxSensors import LinuxSensors
from smartfancontrol.pid.PIDNN.PIDNNFanSpeedCurve import PIDNNFanSpeedCurve
from smartfancontrol.pid.PIDNN.PIDNN import PIDNN
from sfc.ControlLoop import ControlLoop


if __name__ == '__main__':
    server = IPMIToolSSH(
        host='192.168.0.177',
        port=22,
        username='jdsrv',
        password="$Guatemala2016",
        commands=DellIDRAC6(),
        tempsensor=LinuxSensors()
    )

    fanprofile = PIDNNFanSpeedCurve(PIDNN(2, 0.05, 50))

    def hook(**kwargs):
        print(kwargs)

    control = ControlLoop(server, fanprofile, cycleHook=hook)

    control.start()




