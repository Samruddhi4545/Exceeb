from sqlalchemy.orm import Session #type:ignore
from app.models.user import User
from app.models.department import Department


def generate_employee_id(db: Session, batch_number: str, location_code: str, department_id: int) -> str:
    """Generates an employee ID formatted as Batch + Location + Dept + Seq (e.g., 1MAME01)."""
    dept = db.query(Department).filter(Department.id == department_id).first()
    dept_code = dept.code if dept else "XX"

    # Count existing users in this department to calculate sequence
    seq_count = db.query(User).filter(User.department_id == department_id).count() + 1
    seq_str = f"{seq_count:02d}"  # Pad with leading zero (01, 02, etc.)

    return f"{batch_number}{location_code.upper()}{dept_code.upper()}{seq_str}"