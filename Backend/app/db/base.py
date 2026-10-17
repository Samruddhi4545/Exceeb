# Import base class
from app.db.session import Base  # noqa

# Import all models here so Alembic can discover them for migrations
# As you build each model file in Phase 1 & 2, uncomment these imports:
# from app.models.user import User, Role  # noqa
# from app.models.department import Department  # noqa
# from app.models.team import Team  # noqa
# from app.models.campaign import Campaign  # noqa
# from app.models.task import Task, TaskSubmission  # noqa
# from app.models.tracking import WorkSession, Attendance, Location, Geofence  # noqa