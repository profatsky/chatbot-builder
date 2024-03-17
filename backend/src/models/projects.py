import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class ProjectModel(Base):
    __tablename__ = 'projects'

    project_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    user: Mapped['UserModel'] = relationship(back_populates='projects')

    dialogues: Mapped[list['DialogueModel']] = relationship(back_populates='project')
