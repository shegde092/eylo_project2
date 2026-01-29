# Redis Setup for Windows

## The Problem

The in-memory queue doesn't work because the API server and worker run in **separate processes** with separate memory. Jobs created by the API never reach the worker.

**Solution:** Use Redis for a shared queue.

---

## Option 1: Redis via Docker (Recommended)

### Install Docker Desktop
1. Download from: https://www.docker.com/products/docker-desktop/
2. Install and start Docker Desktop

### Run Redis
```powershell
docker run -d -p 6379:6379 --name eylo-redis redis
```

### Update `.env`
```
REDIS_URL=redis://localhost:6379
```

### Restart API and Worker
```powershell
# Terminal 1
python -m app.main

# Terminal 2
python -m app.worker
```

---

## Option 2: Redis for Windows (Memurai)

### Download Memurai
https://www.memurai.com/get-memurai

### Install and Start Service

### Update `.env`
```
REDIS_URL=redis://localhost:6379
```

---

## Option 3: Quick Test Without Redis

For immediate testing, we can modify the queue to use a file-based queue:

### Create `shared_queue.json`
This will act as a simple shared queue between processes.

### Update queue implementation
Use file-based storage instead of in-memory deque.

---

## Recommended: Use Option 1 (Docker + Redis)

This is how production systems work and it's the cleanest solution.
