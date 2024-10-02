from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from database import Metric
from database.session import get_db


class MetricRepository:
    """
    This class handles database operations related to metrics.
    It provides a method to retrieve all metrics from the database.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the MetricRepository with a database session.
        """
        self.db = db

    def get_metrics(self) -> List[Metric]:
        """
        Retrieves all metrics from the database.
        Returns:
            List[Metric]: A list of all metrics.
        """
        metrics = self.db.query(Metric).all()
        return metrics

    def get_metric_by_name(self, metric_name: str) -> Metric:
        """
        Retrieves a metric by its name from the database.
        Args:
            metric_name (str): The name of the metric to retrieve.
        Returns:
            Metric: The metric with the specified name.
        """
        metric = self.db.query(Metric).filter(Metric.name == metric_name).first()
        return metric
