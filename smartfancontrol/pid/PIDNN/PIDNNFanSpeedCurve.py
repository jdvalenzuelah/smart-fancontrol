from sfc.FanSpeedCurve import FanSpeedCurve
from smartfancontrol.pid.PIDNN.PIDNN import PIDNN


class PIDNNFanSpeedCurve(FanSpeedCurve):

    def __init__(self, pidnn: PIDNN):
        self.pidnn = pidnn

    def getFanSpeed(self, feedback: float, currentSpeed: int) -> int:
        self.pidnn.update_feedback(feedback)
        self.pidnn.train()
        return int(self.pidnn.act())
