"""
impitool fan control raw commands for dell's IDrac6. Tested on Poweredge R210
"""


class DellIDRAC6:

    def __init__(self, fan: str = None) -> None:
        super().__init__()
        self._fan = fan if fan else '0xff'

    def fanToUpdate(self, fan):
        self._fan = fan

    def manualFancontrolToggleCommand(self, enabled: bool) -> str:
        toggle = '0x00' if enabled else '0x01'
        return f'0x30 0x30 0x01 {toggle}'

    def fanSpeedCommand(self, speedHex: str) -> str:
        return f'0x30 0x30 0x02 {self._fan} {speedHex}'
