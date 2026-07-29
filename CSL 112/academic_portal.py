"""
CSL 112: Introduction to Advanced Level Programming
Independent Lab Activity: Encapsulation & Secure Class Design

academic_portal.py (Version 2)

Design differences from a "plain getter/setter" implementation:
  - Custom exception types (InvalidRecordError, InvalidCGPAError,
    InvalidPaymentError) instead of raw ValueError, so calling code can
    catch specific failure modes.
  - Private state is exposed internally through Python @property /
    @<name>.setter pairs, and the required public method names
    (get_cgpa, update_cgpa, etc.) are thin wrappers around those
    properties. This keeps the assignment's required interface while
    demonstrating a more idiomatic Pythonic encapsulation pattern.
"""


class InvalidRecordError(ValueError):
    """Raised when a Student is constructed with invalid founding data."""


class InvalidCGPAError(ValueError):
    """Raised when a CGPA value falls outside the valid [0.00, 5.00] range."""


class InvalidPaymentError(ValueError):
    """Raised when a tuition payment amount is not strictly positive."""


class Student:
    """
    Represents a student's academic record.

    Internal state is stored in private attributes and can only be
    reached from outside the class through validated properties /
    accessor methods.
    """

    MIN_CGPA = 0.00
    MAX_CGPA = 5.00

    def __init__(self, matric_no: str, name: str, initial_balance: float):
        if not isinstance(matric_no, str) or not matric_no.strip():
            raise InvalidRecordError(
                "matric_no must be a non-empty string."
            )
        if not isinstance(name, str) or not name.strip():
            raise InvalidRecordError("name must be a non-empty string.")
        if not isinstance(initial_balance, (int, float)):
            raise InvalidRecordError("initial_balance must be numeric.")
        if initial_balance < 0:
            raise InvalidRecordError(
                f"initial_balance cannot be negative (got {initial_balance})."
            )

        self.__matric_number = matric_no
        self.__full_name = name
        self.__cgpa = self.MIN_CGPA
        self.__tuition_balance = float(initial_balance)

    # ------------------------------------------------------------------
    # Pythonic property layer (still private-backed)
    # ------------------------------------------------------------------
    @property
    def cgpa(self) -> float:
        return self.__cgpa

    @cgpa.setter
    def cgpa(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise InvalidCGPAError("CGPA must be numeric.")
        if not (self.MIN_CGPA <= value <= self.MAX_CGPA):
            raise InvalidCGPAError(
                f"CGPA {value} out of bounds "
                f"[{self.MIN_CGPA:.2f}, {self.MAX_CGPA:.2f}]."
            )
        self.__cgpa = float(value)

    @property
    def tuition_balance(self) -> float:
        return self.__tuition_balance

    # ------------------------------------------------------------------
    # Required public interface (spec-mandated method names)
    # ------------------------------------------------------------------
    def get_matric_number(self) -> str:
        return self.__matric_number

    def get_full_name(self) -> str:
        return self.__full_name

    def get_cgpa(self) -> float:
        return self.cgpa

    def get_tuition_balance(self) -> float:
        return self.tuition_balance

    def update_cgpa(self, new_cgpa: float) -> None:
        """Validated mutator — delegates to the cgpa property setter."""
        self.cgpa = new_cgpa

    def pay_tuition(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise InvalidPaymentError("Payment amount must be numeric.")
        if amount <= 0:
            raise InvalidPaymentError(
                f"Payment amount must be greater than zero (got {amount})."
            )
        self.__tuition_balance -= amount

    # ------------------------------------------------------------------
    # Lifecycle management
    # ------------------------------------------------------------------
    def __del__(self):
        matric = getattr(self, "_Student__matric_number", "UNKNOWN")
        print(f"[SESSION CLOSED] Student record for {matric} safely deallocated.")

    def __repr__(self):
        return (
            f"<Student {self.__matric_number} | {self.__full_name} | "
            f"CGPA={self.__cgpa:.2f} | Balance={self.__tuition_balance:.2f}>"
        )


class Department:
    """An academic department that manages a private roster of Students."""

    def __init__(self, dept_name: str):
        if not isinstance(dept_name, str) or not dept_name.strip():
            raise InvalidRecordError("dept_name must be a non-empty string.")
        self.dept_name = dept_name
        self.__students_list = []

    def add_student(self, student_object: Student) -> None:
        if not isinstance(student_object, Student):
            raise TypeError(
                f"Expected a Student instance, got {type(student_object).__name__}."
            )
        self.__students_list.append(student_object)

    def get_students(self) -> list:
        return list(self.__students_list)

    def generate_honors_roll(self, threshold: float = 3.50) -> list:
        print(f"\n--- {self.dept_name} Department: Honors Roll (CGPA >= {threshold:.2f}) ---")
        honors = [s for s in self.__students_list if s.get_cgpa() >= threshold]

        if honors:
            for s in honors:
                print(f"  {s.get_full_name()} ({s.get_matric_number()}): {s.get_cgpa():.2f}")
        else:
            print("  No students currently qualify for the honors roll.")

        print("-------------------------------------------------------------\n")
        return honors
