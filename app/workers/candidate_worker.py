#import asyncio
#import json
#import logging
#from redis.asyncio import Redis
#from app.services.candidate_service import process_candidate_task
#
#
#logger = logging.getLogger(__name__)
#
#REDIS_TASK_QUEUE = "task_queue"
#REDIS_LOCK_PREFIX = "lock:candidate:"
#LOCK_TTL = 60  # seconds
#POLL_INTERVAL = 5  # seconds
#
#class CandidateTaskWorker:
#	def __init__(self, redis: Redis):
#		self.redis = redis
#		self.running = False
#
#
#	async def acquire_lock(self, candidate_id: int) -> bool:
#        key = f"{REDIS_LOCK_PREFIX}{candidate_id}"
#        result = await self.redis.set(
#            key, "locked", ex=LOCK_TTL, nx=True
#        )
#        return result is True
#
#    async def release_lock(self, candidate_id: int):
#        key = f"{REDIS_LOCK_PREFIX}{candidate_id}"
#        await self.redis.delete(key)
#
#    async def process_task(self, task_data: dict):
#        candidate_id = task_data["candidate_id"]
#        got_lock = await self.acquire_lock(candidate_id)
#        if not got_lock:
#            logger.info(f"Lock for candidate {candidate_id} is held, skipping.")
#            return
#
#        try:
#            logger.info(f"Processing task for candidate {candidate_id}")
#            await process_candidate_task(task_data)
#        except Exception as e:
#            logger.error(f"Error processing task: {e}")
#        finally:
#            await self.release_lock(candidate_id)
#
#    async def run(self):
#        self.running = True
#        logger.info("Task worker started.")
#        while self.running:
#            task_json = await self.redis.lpop(REDIS_TASK_QUEUE)
#            if task_json:
#                try:
#                    task_data = json.loads(task_json)
#                    await self.process_task(task_data)
#                except json.JSONDecodeError:
#                    logger.warning("Invalid task format")
#            else:
#                await asyncio.sleep(POLL_INTERVAL)
#
#    def stop(self):
#        self.running = False
#
#
## THIS GOES IN MAIN
#from fastapi import FastAPI
#from redis.asyncio import Redis
#from app.services.task_worker import TaskWorker
#
#app = FastAPI()
#redis = Redis(host="localhost", port=6379, decode_responses=True)
#task_worker = TaskWorker(redis)
#
#@app.on_event("startup")
#async def startup_event():
#    asyncio.create_task(task_worker.run())
#
#@app.on_event("shutdown")
#async def shutdown_event():
#    task_worker.stop()
#    await redis.close()
#
#
## THIS GOES IN CANDIDATE ROUTES
#from redis.asyncio import Redis
#import json
#
#redis = Redis(host="localhost", port=6379, decode_responses=True)
#
#async def queue_task(candidate_id: int, task_payload: dict):
#    task_data = {
#        "candidate_id": candidate_id,
#        "payload": task_payload
#    }
#    await redis.rpush("task_queue", json.dumps(task_data))
#
#
## THIS GOES IN CANDIDATE SERVICE
#async def process_candidate_task(task_data: dict):
#    # Replace this with your actual logic
#    candidate_id = task_data["candidate_id"]
#    payload = task_data["payload"]
#    print(f"Processing candidate {candidate_id} with payload: {payload}")
#    await asyncio.sleep(2)  # simulate work
#
