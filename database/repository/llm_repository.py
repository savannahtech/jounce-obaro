from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from database import LLM
from database.session import get_db


class LLMRepository:
    """
    This class handles database operations related to LLMs.
    It provides a method to retrieve all LLMs from the database.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the LLMRepository with a database session.
        """
        self.db = db

    def get_llms(self) -> List[LLM]:
        """
        Retrieves all LLMs from the database.
        Returns:
            List[LLM]: A list of all LLMs.
        """
        llms = self.db.query(LLM).all()
        return llms
