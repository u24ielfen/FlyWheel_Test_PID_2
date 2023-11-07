from subsystems.flywheel import Flywheel
from commands.flywheel_cmd import Flywheel_CMD


class RobotContainer:
    def __init__(self) -> None:
        self.configure_button_bindings()
        self.flywheel = Flywheel()
        self.flywheel.setDefaultCommand(Flywheel_CMD(self.flywheel))

    def configure_button_bindings(self):
        pass
