# Locust Load Testing with Docker: A Step-by-Step Guide

This guide will help you set up and run Locust load tests using Docker. It covers everything from modifying your Locust script and Dockerfile to running master and worker containers, monitoring memory usage, and troubleshooting common issues.

## Step-by-Step Instructions

### 1. Modify and Save Your Locust Script
Ensure your Locust script is ready. You can name it anything, such as `basic_http_post.py`, but remember the name for the Dockerfile.

### 2. Modify the Dockerfile
Update the Dockerfile to copy your Locust script into the container and always rename it to `/locustfile.py` inside the container.

**Example Dockerfile**:
```dockerfile
FROM locustio/locust

COPY basic_http_post.py /locustfile.py
```
Replace `basic_http_post.py` with your actual script name. The `/locustfile.py` on the right side must stay the same.

### 3. Build the Docker Image
Run this command to build the Docker image:
```bash
docker build -t fukuiz-image .
```
- **fukuiz-image**: You can choose any name for the Docker image. Use the same name consistently when running the containers.

### 4. Run the Locust Master
Run the following command to start the Locust master container:
```bash
docker run --name fukuiz-master fukuiz-image -f /locustfile.py --master --headless -u 1 -r 1 --run-time 1m
```
- **--name fukuiz-master**: The master container's name, which you can choose. Keep it consistent when you link the worker.
- **fukuiz-image**: This is the Docker image name from step 3.
- **-f /locustfile.py**: This always refers to `/locustfile.py` inside the container.
- Adjust **-u** (number of users) and **-r** (spawn rate) to fit your test.

### 5. Run the Locust Worker
Run the following command to start the worker container:
```bash
docker run --name fukuiz-worker --link fukuiz-master:locust-master fukuiz-image -f /locustfile.py --worker --master-host fukuiz-master
```
- **--name fukuiz-worker**: The worker container name, which you can choose.
- **--link fukuiz-master:locust-master**: This links the worker to the master. Ensure the master container name matches.
- **--worker --master-host fukuiz-master**: The master-host option must match the name of the master container.

### 6. Monitor Memory Usage
#### Option 1: Use `docker stats` During the Test
While the load test is running, use the following command to monitor memory and CPU usage:
```bash
docker stats fukuiz-worker
```
This shows live memory usage during the test. Once the test ends, the container will stop, and you won't be able to see the stats.

#### Option 2: Keep the Container Alive After the Test
To keep the worker container alive after the test, append `tail -f /dev/null` to the worker command:
```bash
docker run --name fukuiz-worker --link fukuiz-master:locust-master fukuiz-image -f /locustfile.py --worker --master-host fukuiz-master tail -f /dev/null
```
This keeps the worker container running after the test ends, allowing you to continue checking resource usage with `docker stats`.

### 7. Clean Up Containers and Images
If you need to run new tests or start fresh, clean up old containers:
```bash
docker stop fukuiz-master
docker rm fukuiz-master
docker stop fukuiz-worker
docker rm fukuiz-worker
```
To remove an image (optional):
```bash
docker rmi fukuiz-image
```

## Key Notes on Naming
- **Image Name**: The Docker image name (e.g., `fukuiz-image`) can be anything. Use it consistently when creating containers.
- **Container Names**: The container names (e.g., `fukuiz-master` and `fukuiz-worker`) can be customized. Ensure the worker uses the correct `--link` and `--master-host` options.
- **Locustfile**: Always copy your script as `/locustfile.py` inside the Docker container using the Dockerfile.

## Troubleshooting Common Issues
- **"Waiting for workers to be ready"**: Ensure the master and worker are linked correctly, and the names used in `--link` and `--master-host` match.
- **"Container name already in use"**: Stop and remove the existing container or choose a new name:
```bash
docker stop fukuiz-master
docker rm fukuiz-master
```

---

This guide is designed to make running Locust tests using Docker straightforward. Feel free to use and modify as needed!
