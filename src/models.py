import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from src.db import Base


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    dni: Mapped[str] = Column(String, nullable=False)
    fullname: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, nullable=False)

    _punchs: Mapped[List["Punch"]] = relationship("Punch")

    enrolls: Mapped[Optional["Enrollments"]] = relationship(
        "Enrollments", uselist=False
    )

    def has_enrollments(self) -> bool:
        return True if self.enrolls else False

    def has_pin_enrollment(self) -> bool:
        return True if self.enrolls.pin else False

    def has_same_pin(self, pin: str | int) -> bool:
        return self.enrolls.is_same_pin(pin)

    @property
    def enrolados(self):
        if self.enrolls:
            return {
                "employee_id": self.enrolls.employee_id,
                "pin": self.enrolls.pin,
            }
        return None

    @enrolados.setter
    def enrolados(self, value):
        self.enrolls = value


class Enrollments(Base):
    __tablename__ = "enrollments"

    employee_id: Mapped[int] = Column(
        Integer, ForeignKey("employee.id"), primary_key=True
    )
    pin: Mapped[Optional[str]] = Column(String, nullable=True)

    def is_same_pin(self, pin: str | int) -> bool:
        pin = int(pin) if isinstance(pin, str) else pin
        return int(self.pin) == pin


class Devices(Base):
    __tablename__ = "devices"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String)
    location: Mapped[str] = Column(String)
    timezone: Mapped[str] = Column(String)

    punch_type: Mapped["DevicePunchType"] = relationship(
        "DevicePunchType", uselist=False, passive_deletes=True, cascade="all, delete"
    )


    @property
    def pin(self):
        return self.punch_type.pin


class DevicePunchType(Base):
    __tablename__ = "punch_type"

    device_id: Mapped[int] = Column(Integer, ForeignKey("devices.id"), primary_key=True)
    pin: Mapped[bool] = Column(Boolean)


class PunchTypeEnum(str, enum.Enum):
    pin = "pin"


class Punch(Base):
    __tablename__ = "punch"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    device_id: Mapped[int] = Column(Integer, ForeignKey("devices.id"))
    timezone: Mapped[str] = Column(String)
    punch_dtm: Mapped[datetime] = Column(DateTime)
    punch_type: Mapped[PunchTypeEnum] = Column(Enum(PunchTypeEnum))
    dni: Mapped[str] = Column(String)
    status: Mapped[str] = Column(String)
    employee_id: Mapped[Optional[int]] = Column(Integer, ForeignKey("employee.id"))
    pin: Mapped[Optional[str]] = Column(String, nullable=True)
