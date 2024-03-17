import datetime
import enum

from sqlalchemy import String, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class DialogueModel(Base):
    __tablename__ = 'dialogues'

    dialogue_id: Mapped[int] = mapped_column(primary_key=True)

    trigger_id: Mapped[int] = mapped_column(ForeignKey('triggers.trigger_id', ondelete='RESTRICT'))
    trigger: Mapped['TriggerModel'] = relationship(back_populates='dialogue')

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.project_id', ondelete='CASCADE'))
    project: Mapped['ProjectModel'] = relationship(back_populates='dialogues')

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # TODO add template_id


class TriggerEventType(enum.Enum):
    TEXT = 'text'
    COMMAND = 'command'
    BUTTON = 'button'


class TriggerModel(Base):
    __tablename__ = 'triggers'

    trigger_id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[TriggerEventType] = mapped_column(Enum(TriggerEventType).values_callable, nullable=False)
    value: Mapped[str] = mapped_column(String(64))

    dialogue: Mapped[DialogueModel] = relationship(back_populates='trigger')
