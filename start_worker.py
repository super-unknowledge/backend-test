import asyncio
from app.workers.candidate_worker import worker_loop

if __name__ == "__main__":
    asyncio.run(worker_loop())

