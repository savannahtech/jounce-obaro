from sqlalchemy import Column, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.base_class import Base


class Simulation(Base):
    __tablename__ = "simulations"
    value = Column(Float, nullable=False)
    llm_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)
    metric_id = Column(UUID(as_uuid=True), ForeignKey("metrics.id"), nullable=False)

    llm = relationship("LLM")
    metric = relationship("Metric")

    # Add indexes
    __table_args__ = (
        Index("ix_simulations_llm_id", llm_id),
        Index("ix_simulations_metric_id", metric_id),
    )

    def __repr__(self):
        return (
            f"<Simulation(id={self.id}, value={self.value}, llm_id={self.llm_id}, "
            f"metric_id={self.metric_id}, llm={self.llm}, metric={self.metric}>"
        )
