"""
CSL 112: Introduction to Advanced Level Programming
Independent Lab Activity: Encapsulation & Secure Class Design

main.py (Version 2)
Edge-case testing suite built on Python's unittest framework.
Run with:  python3 -m unittest main.py -v
or simply: python3 main.py
"""

import unittest

from academic_portal import (
    Student,
    Department,
    InvalidRecordError,
    InvalidCGPAError,
)


class TestStudentConstruction(unittest.TestCase):

    def test_negative_tuition_balance_rejected(self):
        """Test 1: negative starting balance must fail gracefully."""
        with self.assertRaises(InvalidRecordError):
            Student("FUEP/CSC/24/001", "Malicious Actor", -5000.00)

    def test_empty_matric_number_rejected(self):
        with self.assertRaises(InvalidRecordError):
            Student("", "No Matric", 1000.00)

    def test_valid_construction_succeeds(self):
        s = Student("FUEP/CSC/24/002", "Abel Danjuma", 50000.00)
        self.assertEqual(s.get_tuition_balance(), 50000.00)
        self.assertEqual(s.get_cgpa(), 0.00)


class TestEncapsulation(unittest.TestCase):

    def test_direct_attribute_tampering_is_ineffective(self):
        """Test 2: writing to student.__cgpa from outside the class must
        NOT alter the real internal state (Python name-mangling)."""
        student1 = Student("FUEP/CSC/24/003", "Chiamaka Obi", 30000.00)

        # setattr() is used here (instead of student1.__cgpa = 4.9) purely
        # because this line sits inside a test *class* body, where Python
        # would mangle the literal '__cgpa' a second time. setattr() writes
        # the exact string "__cgpa", reproducing what an external attacker
        # typing student1.__cgpa = 4.9 at the top level would actually do.
        setattr(student1, "__cgpa", 4.9)  # creates a decoy public attribute

        self.assertEqual(student1.get_cgpa(), 0.00)
        self.assertIn("__cgpa", student1.__dict__)          # the decoy exists
        self.assertIn("_Student__cgpa", student1.__dict__)  # the real field, untouched
        self.assertNotEqual(student1.__dict__["_Student__cgpa"], 4.9)


class TestCGPAValidation(unittest.TestCase):

    def setUp(self):
        self.student = Student("FUEP/CSC/24/004", "Emeka Okafor", 15000.00)

    def test_cgpa_above_max_rejected(self):
        """Test 3: update_cgpa(6.0) must be rejected."""
        with self.assertRaises(InvalidCGPAError):
            self.student.update_cgpa(6.0)

    def test_cgpa_below_min_rejected(self):
        with self.assertRaises(InvalidCGPAError):
            self.student.update_cgpa(-1.5)

    def test_cgpa_boundary_values_accepted(self):
        self.student.update_cgpa(0.00)
        self.assertEqual(self.student.get_cgpa(), 0.00)
        self.student.update_cgpa(5.00)
        self.assertEqual(self.student.get_cgpa(), 5.00)


class TestDepartmentHonorsRoll(unittest.TestCase):

    def test_honors_roll_with_three_valid_students(self):
        """Test 4: add 3 valid students and generate the honors roll."""
        dept = Department("Computer Science")

        s1 = Student("FUEP/CSC/24/005", "Grace Musa", 20000.00)
        s2 = Student("FUEP/CSC/24/006", "Ibrahim Sule", 15000.00)
        s3 = Student("FUEP/CSC/24/007", "Fatima Bello", 0.00)

        s1.update_cgpa(4.20)  # qualifies
        s2.update_cgpa(3.10)  # does not qualify
        s3.update_cgpa(3.75)  # qualifies

        dept.add_student(s1)
        dept.add_student(s2)
        dept.add_student(s3)

        self.assertEqual(len(dept.get_students()), 3)

        honors = dept.generate_honors_roll()
        honor_names = {s.get_full_name() for s in honors}

        self.assertEqual(honor_names, {"Grace Musa", "Fatima Bello"})

    def test_department_rejects_non_student_objects(self):
        dept = Department("Computer Science")
        with self.assertRaises(TypeError):
            dept.add_student("not a real student")


if __name__ == "__main__":
    unittest.main(verbosity=2)
