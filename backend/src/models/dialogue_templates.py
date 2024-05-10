import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class DialogueTemplateModel(Base):
    __tablename__ = 'templates'

    template_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(128), unique=True)
    summary: Mapped[str] = mapped_column(String(512))
    description: Mapped[str] = mapped_column(String(4096))
    image_path: Mapped[str] = mapped_column(String(512))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    dialogue_id: Mapped[int] = mapped_column(ForeignKey('dialogues.dialogue_id', ondelete='CASCADE'))
    dialogue: Mapped['DialogueModel'] = relationship(back_populates='template')
