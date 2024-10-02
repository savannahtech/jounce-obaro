import asyncio
import os
from contextlib import asynccontextmanager
from threading import Thread

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from fastapi import FastAPI

from database import (
    Base,
    LLMRepository,
    MetricRepository,
    SimulatorRepository,
    settings_config,
)
from database.seed import seed_data
from database.session import engine, get_db
from logger import logging
from metric_simulator.metric_service import MetricService

load_dotenv()

scheduler = AsyncIOScheduler()
main_loop = asyncio.get_event_loop()

SCHEDULE_INTERVAL = os.getenv("SCHEDULE_INTERVAL", "3")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application(lifespan):
    app = FastAPI(
        title=settings_config.PROJECT_NAME,
        version=settings_config.PROJECT_VERSION,
        lifespan=lifespan,
    )
    create_tables()
    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    # seed initial app data
    seed_data(db)
    llm_repository = LLMRepository(db)
    metric_repository = MetricRepository(db)
    simulator_repository = SimulatorRepository(db)
    metric_service = MetricService(
        llm_repository, metric_repository, simulator_repository
    )

    async def run_simulate_data_points():
        await metric_service.simulate_data_points_with_retry()

    def run_scheduler():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def schedule_task():
            asyncio.run_coroutine_threadsafe(run_simulate_data_points(), main_loop)

        scheduler.add_job(schedule_task, "interval", minutes=int(SCHEDULE_INTERVAL))
        scheduler.start()
        loop.run_forever()

    asyncio.create_task(run_simulate_data_points())

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

    yield

    # Shutdown
    scheduler.shutdown()
    scheduler_thread.join(timeout=10)  # Wait up to 10 seconds for the thread to finish
    if scheduler_thread.is_alive():
        logging.info("Warning: Scheduler thread did not shut down cleanly")
    logging.info("Scheduler shutdown complete")


app = start_application(lifespan)
