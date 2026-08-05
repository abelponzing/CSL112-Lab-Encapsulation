"""
test_inheritance.py
CSL 112 - Independent Lab Activity: Inheritance, Polymorphism & Abstract Classes

Verifies polymorphic (dynamic-dispatch) behaviour of the User hierarchy
defined in institutional_system.py, and confirms the abstract-class
contract rules from Part 4.
"""

from institutional_system import User, StudentUser, LecturerUser, ResearchAssistant


def build_payroll_queue():
    """Create a mixed list of concrete User subclass instances."""
    student = StudentUser(
        user_id="STU001",
        full_name="Abel Danladi",
        email="abel.danladi@fuep.edu.ng",
        stipend_rate=45000.00,
        courses_enrolled=6,
    )

    lecturer = LecturerUser(
        user_id="LEC001",
        full_name="Dr. Grace Okoro",
        email="g.okoro@fuep.edu.ng",
        base_salary=250000.00,
        overtime_hours=8,
        hourly_rate=3500.00,
    )

    research_assistant = ResearchAssistant(
        user_id="RA001",
        full_name="Musa Ibrahim",
        email="m.ibrahim@fuep.edu.ng",
        stipend_rate=50000.00,
        courses_enrolled=4,
        research_grant_allowance=15000.00,
    )

    # A single list holding different concrete types under one common
    # base-class interface (User). This is the polymorphic container.
    payroll_queue = [student, lecturer, research_assistant]
    return payroll_queue


def run_payroll(payroll_queue):
    """
    Iterate the queue and call calculate_monthly_payout() on every object
    WITHOUT checking (isinstance / type()) what concrete class it is.

    ---------------------------------------------------------------------
    POLYMORPHIC TEST NOTE (dynamic dispatch):
    Even though the loop below only ever "sees" the object through its
    User interface, Python resolves calculate_monthly_payout() at RUNTIME
    based on the object's actual (concrete) class, not on the reference
    type. So:
        - when `user` is really a StudentUser        -> StudentUser's version runs
        - when `user` is really a LecturerUser        -> LecturerUser's version runs
        - when `user` is really a ResearchAssistant   -> ResearchAssistant's version runs
    This is dynamic dispatch / runtime polymorphism: the SAME line of code
    (`user.calculate_monthly_payout()`) automatically routes to different
    method implementations depending on the object's real type.
    ---------------------------------------------------------------------
    """
    total_payout = 0.0
    print("=== Monthly Payroll Run ===")
    for user in payroll_queue:  # `user` is typed as User, but holds any subclass
        payout = user.calculate_monthly_payout()  # dynamic dispatch happens here
        total_payout += payout
        print(f"{user}  ->  Payout: NGN {payout:,.2f}")
    print(f"Total payroll for this run: NGN {total_payout:,.2f}\n")
    return total_payout


def test_abstract_class_cannot_be_instantiated():
    try:
        User("X000", "Should Fail", "fail@fuep.edu.ng")
        print("[FAIL] User() should not have been instantiable.")
    except TypeError:
        print("[PASS] Direct instantiation of abstract class User correctly raised TypeError.")


def test_incomplete_subclass_cannot_be_instantiated():
    class BrokenUser(User):
        # Does NOT override calculate_monthly_payout()
        pass

    try:
        BrokenUser("X001", "Broken", "broken@fuep.edu.ng")
        print("[FAIL] BrokenUser() should not have been instantiable.")
    except TypeError:
        print("[PASS] Subclass missing calculate_monthly_payout() correctly raised TypeError.")


if __name__ == "__main__":
    queue = build_payroll_queue()
    run_payroll(queue)
    test_abstract_class_cannot_be_instantiated()
    test_incomplete_subclass_cannot_be_instantiated()
