import asyncio
import json
from app.utils.redis import redis_client

async def test_enqueue():
    task = {
        "candidate_id": "6e8bfd00-2473-4b40-94de-afffee3554aa",
        "task_type": "resume_parsing",
        "metadata": {"source": "manual test"}
    }
    await redis_client.rpush("candidate:processing_queue", json.dumps(task))
    print("Task enqueued!")

if __name__ == "__main__":
    asyncio.run(test_enqueue())

