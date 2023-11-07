from commands2 import SubsystemBase
from rev import CANSparkMax, CANSparkMaxLowLevel, SparkMaxAbsoluteEncoder
from constants import FlyWheelConstants
from wpilib import SmartDashboard


class Flywheel(SubsystemBase):
    def __init__(self) -> None:
        super().__init__()
        self.motor = CANSparkMax(
            FlyWheelConstants.MotorID, CANSparkMaxLowLevel.MotorType.kBrushless
        )
        self.motor.restoreFactoryDefaults()
        self.motor_encoder = self.motor.getEncoder()
        self.pidController = self.motor.getPIDController()

        self.kP = 5e-5  # 0.00002
        self.kI = 1e-6  # 0.00000000015
        self.kD = 0.0
        self.kFF = 0.000156  # 0.00000481

        self.pidController.setP(self.kP)
        self.pidController.setI(self.kI)
        self.pidController.setD(self.kD)

        self.pidController.setIZone(0.0)
        self.pidController.setFF(self.kFF)
        self.pidController.setOutputRange(-1, 1)

        self.setPoint = 0.0

        self.mode = True
        SmartDashboard.putNumber("kP", self.kP)
        SmartDashboard.putNumber("kI", self.kI)
        SmartDashboard.putNumber("kD", self.kD)
        SmartDashboard.putNumber("kFF", self.kFF)
        SmartDashboard.putBoolean("Mode", self.mode)

    def setMode(self, mode: bool) -> None:
        self.mode = mode

    def periodic(self) -> None:
        self.p = SmartDashboard.getNumber("kP", 0.0)
        self.i = SmartDashboard.getNumber("kI", 0.0)
        self.d = SmartDashboard.getNumber("kD", 0.0)
        self.kF = SmartDashboard.getNumber("kFF", 0.0)
        self.stPt = SmartDashboard.putNumber("Setpoint", 0.0)
        if self.p != self.kP:
            self.pidController.setP(self.p)
        if self.i != self.kI:
            self.pidController.setP(self.i)
        if self.d != self.kD:
            self.pidController.setP(self.d)
        if self.kF != self.kFF:
            self.pidController.setP(self.kFF)

        if self.mode:
            self.pidController.setReference(
                SmartDashboard.getNumber("SetPoint", 0.0),
                CANSparkMax.ControlType.kVelocity,
            )
            self.measurement = self.motor_encoder.getVelocity()
        else:
            self.pidController.setReference(
                SmartDashboard.getNumber("SetPoint", 0.0),
                CANSparkMax.ControlType.kPosition,
            )
            self.measurement = self.motor_encoder.getPosition()
        SmartDashboard.putNumber("Measured Position", self.motor_encoder.getPosition())
        SmartDashboard.putNumber("Measured Velocity", self.motor_encoder.getVelocity())
        SmartDashboard.putNumber("Output", self.motor.getAppliedOutput())

    def get_error(self) -> float:
        return SmartDashboard.getNumber("SetPoint", 0.0) - self.measurement

    def stop_flywheel(self) -> None:
        self.motor.set(0.0)
