from paramiko.client import SSHClient
from smartfancontrol.server.shellutils import scapeStr
from smartfancontrol.server.ipmi.DellIDRAC6 import DellIDRAC6
from smartfancontrol.server.linux.LinuxSensors import LinuxSensors
from sfc.CommunicationBuffer import CommunicationBuffer

"""
Implementation to DellIDRAC6 and LinuxSensors over ssh

requires impitool and sensors to be installed in target host
"""


class IPMIToolSSH(CommunicationBuffer):

    def __init__(self, host: str, port: int, username: str, password: str, commands: DellIDRAC6,
                 tempsensor: LinuxSensors, require_sudo=True, ipmitool="ipmitool") -> None:
        super().__init__()
        self._commands = commands
        self._tempsensor = tempsensor
        self.require_sudo = require_sudo
        self.ipmitool = ipmitool
        self._password = password
        self._client = SSHClient()
        self._client.load_system_host_keys()
        self._client.connect(host, port=port, username=username, password=password)

    def __impitoolRawCommand(self, payload: str) -> str:
        return f'{self.ipmitool} raw {payload}'

    def __impitoolCommand(self, payload: str) -> str:
        return f'{self.ipmitool} {payload}'

    def _sudoCommand(self, cmd: str) -> str:
        scaped_pwd = scapeStr(self._password)
        return f'echo {scaped_pwd} | sudo -S {cmd}'

    def execCmd(self, cmd) -> bool:
        return self.__execCmd(cmd)

    def __execCmd(self, cmd):
        cmd = cmd if not self.require_sudo else self._sudoCommand(cmd)
        return self._client.exec_command(cmd)

    def setFanSpeed(self, speed: int):
        if 100 >= speed >= 0:
            # Make sure manual fancontrol is enabled
            cmd = self.__impitoolRawCommand(self._commands.manualFancontrolToggleCommand(True))
            self.__execCmd(cmd)
            cmd = self.__impitoolRawCommand(self._commands.fanSpeedCommand(hex(speed)))
            stdin, stdout, stderr = self.__execCmd(cmd)
            stdout.read()

    def getSystemTemperature(self) -> float:
        _, stdout, stderr = self.__execCmd(self._tempsensor.getCpuTempCommand())
        result = stdout.read().decode('utf-8')
        return self._tempsensor.parseTempResponse(result)

    def getFanSpeed(self) -> int:
        cmd = 'sensor reading "Ambient Temp" "FAN 1 RPM" "FAN 2 RPM" "FAN 3 RPM"'
        _, stdin, stderr = self.__execCmd(self.__impitoolCommand(cmd))
        res = stdin.read().decode('utf-8').split('\n')

        speeds = [int(line.split('|')[-1].strip()) for line in res if 'FAN' in line]

        return int((sum(speeds) / len(speeds)) / 18000)
