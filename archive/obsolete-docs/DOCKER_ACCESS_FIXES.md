# Docker Access Fixes

## Issues Resolved

1. **Images not accessible**: Users reported that images (uploaded or generated) were not accessible from localhost.
2. **Qdrant not accessible**: Users reported inability to access the Qdrant vector database dashboard/API.

## Fixes Applied

### 1. Image Access (Static Files)

- **Updated `docker-compose.prod.yml`**: Added volume mounts for `./uploads` and `./output` to the `nginx` service.
- **Updated `nginx/nginx.conf`**:
  - Added `localhost` to `server_name`.
  - Added location blocks for `/uploads/` and `/output/`.
- **Updated `python-services/api/app.py`**: Mounted `StaticFiles` to serve `/uploads` and `/output` directly from the API (port 8000).

### 2. Qdrant Access

- **Updated `docker-compose.prod.yml`**: Exposed port `6333` for the `qdrant` service.

  ```yaml
  qdrant:
    ports:
      - "6333:6333"
  ```

- **Updated `nginx/nginx.conf`**: Added `qdrant_backend` upstream and a server block for `qdrant.*` subdomain.

## How to Apply Changes

1. Stop the running containers:

   ```bash
   docker-compose -f construction-platform/docker-compose.prod.yml down
   ```

2. Rebuild and start the containers:

   ```bash
   docker-compose -f construction-platform/docker-compose.prod.yml up -d --build
   ```

## Verification

### Images

- Access uploaded files via Nginx: `http://localhost/uploads/filename.ext`
- Access output files via Nginx: `http://localhost/output/filename.ext`

### Qdrant

- Access Qdrant Dashboard: `http://localhost:6333/dashboard`
- Access Qdrant API: `http://localhost:6333`
