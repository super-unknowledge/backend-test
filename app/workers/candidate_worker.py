import asyncio
import json
from app.utils.redis import redis_client
from app.services.candidate_service import process_candidate_task  # assume this handles your task logic

QUEUE_NAME = "candidate:processing_queue"
LOCK_PREFIX = "lock:candidate:"
LOCK_TTL = 30  # seconds
POLL_INTERVAL = 5  # seconds


async def acquire_lock(candidate_id: str) -> bool:
    lock_key = f"{LOCK_PREFIX}{candidate_id}"
    # SETNX: only sets if key doesn't exist
    is_set = await redis_client.set(lock_key, "1", ex=LOCK_TTL, nx=True)
    return is_set is True


async def release_lock(candidate_id: str):
    lock_key = f"{LOCK_PREFIX}{candidate_id}"
    await redis_client.delete(lock_key)


async def worker_loop():
    while True:
        task_raw = await redis_client.lpop(QUEUE_NAME)
        if not task_raw:
            await asyncio.sleep(POLL_INTERVAL)
            continue

        try:
            task = json.loads(task_raw)
            candidate_id = task["candidate_id"]

            # Try to acquire a lock
            if not await acquire_lock(candidate_id):
                # Requeue the task for later
                await redis_client.rpush(QUEUE_NAME, task_raw)
                await asyncio.sleep(POLL_INTERVAL)
                continue

            # Process the task
            try:
                await process_candidate_task(task)
            finally:
                await release_lock(candidate_id)

        except Exception as e:
            # Optionally log this error
            print(f"Error processing task: {e}")

        await asyncio.sleep(0.1)  # Prevent CPU burn

