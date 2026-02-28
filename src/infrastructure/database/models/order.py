import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities import OrderStatus
from src.infrastructure.database import Base


class OrderDB(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    items: Mapped[list[dict]] = mapped_column(JSONB, nullable=False, default=list)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))

    # --------- Связи ---------
    user: Mapped["UserDB"] = relationship("UserDB", back_populates="orders")

    def __repr__(self) -> str:
        return f"OrderDB(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, status={self.status})"
