"""
institutional_system.py
CSL 112 - Independent Lab Activity: Inheritance, Polymorphism & Abstract Classes

Defines an abstract User class and a small institutional hierarchy of
users (StudentUser, LecturerUser, ResearchAssistant) that each implement
their own payroll/payout logic through a shared abstract contract.
"""

from abc import ABC, abstractmethod


class User(ABC):
    """
    Abstract Base Class representing a generic institutional user.

    This class can never be instantiated directly (Python's ABC module
    enforces this at object-creation time). It defines the shared
    attributes every user type needs, plus an abstract method that every
    concrete subclass MUST override.
    """

    def __init__(self, user_id: str, full_name: str, email: str):
        self._user_id = user_id
        self._full_name = full_name
        self._email = email

    # ---------- Concrete (shared) methods ----------
    def get_user_id(self) -> str:
        return self._user_id

    def get_full_name(self) -> str:
        return self._full_name

    def get_email(self) -> str:
        return self._email

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self._full_name} (ID: {self._user_id}, Email: {self._email})"

    # ---------- Abstract contract ----------
    @abstractmethod
    def calculate_monthly_payout(self) -> float:
        """Every subclass MUST provide its own payout calculation."""
        raise NotImplementedError


class StudentUser(User):
    """A student who receives a stipend, minus a fixed welfare deduction."""

    STUDENT_WELFARE_DEDUCTION_RATE = 0.02  # fixed 2% deduction

    def __init__(self, user_id: str, full_name: str, email: str,
                 stipend_rate: float, courses_enrolled: int):
        super().__init__(user_id, full_name, email)
        self.__stipend_rate = stipend_rate
        self.__courses_enrolled = courses_enrolled

    def get_stipend_rate(self) -> float:
        return self.__stipend_rate

    def get_courses_enrolled(self) -> int:
        return self.__courses_enrolled

    def calculate_monthly_payout(self) -> float:
        deduction = self.__stipend_rate * self.STUDENT_WELFARE_DEDUCTION_RATE
        return self.__stipend_rate - deduction


class LecturerUser(User):
    """A lecturer paid a base salary plus overtime."""

    def __init__(self, user_id: str, full_name: str, email: str,
                 base_salary: float, overtime_hours: int, hourly_rate: float):
        super().__init__(user_id, full_name, email)
        self.__base_salary = base_salary
        self.__overtime_hours = overtime_hours
        self.__hourly_rate = hourly_rate

    def get_base_salary(self) -> float:
        return self.__base_salary

    def get_overtime_hours(self) -> int:
        return self.__overtime_hours

    def get_hourly_rate(self) -> float:
        return self.__hourly_rate

    def calculate_monthly_payout(self) -> float:
        return self.__base_salary + (self.__overtime_hours * self.__hourly_rate)


class ResearchAssistant(StudentUser):
    """
    A student who ALSO receives a research grant allowance.

    Demonstrates multi-level inheritance: User -> StudentUser -> ResearchAssistant.
    Reuses (rather than duplicates) StudentUser's payout logic via super().
    """

    def __init__(self, user_id: str, full_name: str, email: str,
                 stipend_rate: float, courses_enrolled: int,
                 research_grant_allowance: float):
        super().__init__(user_id, full_name, email, stipend_rate, courses_enrolled)
        self.__research_grant_allowance = research_grant_allowance

    def get_research_grant_allowance(self) -> float:
        return self.__research_grant_allowance

    def calculate_monthly_payout(self) -> float:
        # Builds on top of StudentUser's own payout calculation.
        base_payout = super().calculate_monthly_payout()
        return base_payout + self.__research_grant_allowance


# ---------------------------------------------------------------------------
# Part 4: Edge case demonstrations (also see test_inheritance.py for asserts)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 1. Attempting to instantiate the abstract User class directly.
    try:
        u = User("U000", "Ghost User", "ghost@fuep.edu.ng")
    except TypeError as e:
        print(f"[Expected] Cannot instantiate abstract class User: {e}")

    # 2. A subclass that forgets to override calculate_monthly_payout()
    #    also cannot be instantiated.
    class IncompleteUser(User):
        pass

    try:
        iu = IncompleteUser("U001", "Incomplete Person", "incomplete@fuep.edu.ng")
    except TypeError as e:
        print(f"[Expected] Cannot instantiate incomplete subclass: {e}")
