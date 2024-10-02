from sqlalchemy import Column, String

from database.base_class import Base


class Metric(Base):
    __tablename__ = "metrics"
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Metric(id={self.id}, name={self.name}>"
