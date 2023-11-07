from commands2 import CommandBase
from subsystems.flywheel import Flywheel
from wpilib import SmartDashboard
from constants import FlyWheelConstants


class Flywheel_CMD(CommandBase):
    def __init__(self, flywheel: Flywheel) -> None:
        super().__init__()
        self.flywheel = flywheel
        self.addRequirements(flywheel)

    def execute(self) -> None:
        self.mode = SmartDashboard.getBoolean("Velocity Mode", True)
        self.flywheel.setMode(self.mode)

    def end(self, interrupted: bool) -> None:
        self.flywheel.stop_flywheel()

    def isFinished(self) -> None:
        if self.mode:
            return self.flywheel.get_error() < FlyWheelConstants.Velocity_Tolerance
        else:
            return self.flywheel.get_error() < FlyWheelConstants.Position_Tolerance
