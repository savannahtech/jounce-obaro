from sqlalchemy import Column, String

from database.base_class import Base


class LLM(Base):
    __tablename__ = "llms"
    name = Column(String, unique=True, nullable=False)
    company_name = Column(String, unique=False, nullable=False)

    def __repr__(self):
        return (
            f"<LLM(id={self.id}, name={self.name}, company_name={self.company_name})>"
        )
