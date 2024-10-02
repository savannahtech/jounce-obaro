from sqlalchemy.orm import Session

from database import LLM, Metric
from logger import logging


def seed_metrics(db: Session):
    if db.query(Metric).count() > 0:
        logging.info("Metrics table is not empty. Seeding skipped.")
        return

    metric_names = [
        "ttft",  # Time to First Token
        "tps",  # Tokens Per Second
        "e2e_latency",  # End-to-End Latency
        "rps",  # Requests Per Second
    ]

    for name in metric_names:
        metric = Metric(name=name)
        db.add(metric)

    db.commit()
    logging.info("Metrics seeded successfully.")


def seed_llms(db: Session):
    if db.query(LLM).count() > 0:
        logging.info("LLM table is not empty. Seeding skipped.")
        return

    llm_names = [
        {"name": "GPT-4o", "company_name": "openai"},
        {"name": "Llama 3.1 70B", "company_name": "meta"},
        {"name": "Claude 3.5 Sonnet", "company_name": "anthropic"},
    ]

    for llm in llm_names:
        llm = LLM(name=llm["name"], company_name=llm["company_name"])
        db.add(llm)

    db.commit()
    logging.info("LLMs seeded successfully.")


def seed_data(db: Session):
    seed_llms(db)
    seed_metrics(db)
