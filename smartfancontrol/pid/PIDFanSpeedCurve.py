from sfc.FanSpeedCurve import FanSpeedCurve
from simple_pid import PID


class PIDFanSpeedCurve(FanSpeedCurve):

    def __init__(self, pid: PID):
        self.pid = pid

    def getFanSpeed(self, feedback: float, currentSpeed: int) -> int:
        return int(self.pid(feedback))
