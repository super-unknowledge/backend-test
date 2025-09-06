# Candidate Management API 

insert project description
---

## Endpoints

| Method | Path         | Description            |
|--------|--------------|------------------------|
| GET    | `/health`    | Health check endpoint  |
| POST   | `/task`      | Add a task to the queue|
| GET    | `/result/{id}` | Get task result       |


---

## Running with Docker

1. **Build and start the containers:**

```bash
docker compose up --build -d
```

access the fastapi docs

stop the containers

test redis queue
docker compose exec web python -m scripts.test_enqueue
or
docker compose exec web PYTHONPATH=. python scripts/test_enqueue.py


docker compose exec redis redis-cli
LRANGE candidate:processing_queue 0 -1
you should see
1) "{\"candidate_id\": \"123\", \"task_type\": \"resume_parsing\", \"metadata\": {\"source\": \"manual test\"}}"

check length of queue
LLEN candidate:processing_queue

