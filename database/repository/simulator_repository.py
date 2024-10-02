from typing import List, Tuple
from uuid import UUID

from fastapi import Depends
from sqlalchemy import func, insert
from sqlalchemy.orm import Session

from database import LLM, Metric, Simulation
from database.session import get_db


class SimulatorRepository:
    """
    This class handles database operations related to simulations.
    It provides methods to get all metrics, bulk add metrics, and remove all metrics.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the SimulatorRepository with a database session.
        """
        self.db = db

    def get_metrics(self) -> List[Simulation]:
        """
        Retrieves all simulation metrics from the database.
        Returns:
            List[Simulation]: A list of all simulation metrics.
        """
        metrics = self.db.query(Simulation).all()
        return metrics

    def bulk_add_metrics(
        self, llm_id: UUID, metric_id: UUID, metrics: List[Simulation]
    ) -> int:
        """
        Bulk adds simulation metrics to the database.
        Args:
            llm_id (UUID): The ID of the LLM.
            metric_id (UUID): The ID of the metric.
            metrics (List[Simulation]): A list of simulation metrics to be added.
        Returns:
            int: The number of metrics added.
        """
        data = [
            {"llm_id": llm_id, "metric_id": metric_id, "value": value}
            for value in metrics
        ]

        # Use SQLAlchemy's bulk insert operation
        self.db.execute(insert(Simulation), data)
        self.db.commit()

        return len(metrics)

    def remove_all_metrics(self) -> None:
        """
        Clears the database of all existing simulation metrics.
        This method executes a bulk deletion of all simulation metrics, ensuring a clean slate for new data.
        Returns:
            None
        """
        self.db.query(Simulation).delete(synchronize_session=False)
        self.db.commit()

    def get_metric_means_by_llm(self, metric_name: str) -> List[Tuple[str, str, float]]:
        """
        Retrieves the mean simulation metric values for given metric.

        Args:
            metric_name (str): The name of the metric to filter by. If not provided, all metrics are considered.

        Returns:
            List[Tuple[str, str, float]]: A list of tuples containing the LLM name, metric name,
            and the mean metric value.
        """
        query = (
            self.db.query(
                LLM.name.label("llm_name"),
                func.avg(Simulation.value).label("mean_value"),
            )
            .join(Simulation.llm)
            .join(Simulation.metric)
            .filter(Metric.name == metric_name)
            .group_by(LLM.name, Metric.name)
            .order_by(func.avg(Simulation.value).desc())
        )

        return query.all()
