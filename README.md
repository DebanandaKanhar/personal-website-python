# Python Personal Website (Standalone Project)

This project is a Python rewrite of your personal website with:

- Web UI (home, articles, article detail, admin portal)
- API layer for posts/categories/admin/analytics
- Postgres-ready data models
- Docker + CI/CD workflow
- Starter MLOps pipeline for article recommendations

## 1) Quick start (one command)

```bash
./scripts/bootstrap.sh
./scripts/start_local.sh
```

Open:

- Web app: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`
- API docs: `http://localhost:8000/docs`

Note: local quick start uses SQLite by default (no Postgres required).

## 2) One-click docker deployment

```bash
./scripts/deploy_local_docker.sh
```

Docker mode runs Postgres + API together.

## 3) Routes overview

Web routes:

- `GET /`
- `GET /articles`
- `GET /articles/{slug}`
- `GET /admin`

API routes:

- `GET /api/categories`
- `GET /api/posts?cat=&q=&status=`
- `GET /api/posts/{slug}`
- `POST /api/admin/login`
- `GET /api/admin/posts`
- `POST /api/admin/posts`
- `PUT /api/admin/posts/{post_id}`
- `DELETE /api/admin/posts/{post_id}`
- `POST /api/analytics/pageview`
- `GET /api/analytics/stats?type=overview|daily-views|top-pages|devices|browsers`

## 4) Publish and productionize (DevOps)

Use this sequence for production:

1. **Containerize and scan**
   - Build image with `docker build`.
   - Add security scan stage (e.g. Trivy) in CI.
2. **Provision infrastructure**
   - Managed Postgres (AWS RDS / Neon / Supabase Postgres).
   - App runtime (AWS ECS Fargate / Render / Fly.io / GKE).
3. **Secrets and config**
   - Store env vars in secret manager (AWS Secrets Manager/GitHub Environments).
   - Never commit `.env`.
4. **CI/CD**
   - On PR: install deps, tests, lint, build image.
   - On main: deploy to staging, run smoke tests, manual approval -> prod.
5. **Observability**
   - Health endpoint: `/healthz`.
   - Metrics endpoint (Prometheus): `/metrics`.
   - Add logs + alerts for error rate, latency, DB failures.
6. **Reliability**
   - Blue/green or rolling deploy.
   - DB backups, migration rollback, SLO alerts.

Quick publish option (Render):

1. Push this project to a GitHub repository.
2. In Render, deploy Blueprint using `render.yaml`.
3. Set `ADMIN_EMAIL` and `ADMIN_PASSWORD`.
4. Validate `/healthz` after deploy.

## 5) MLOps steps for this app

This repo includes a simple recommendation pipeline:

- Training: `ml/recommendation_training.py`
- Inference helper: `ml/recommendation_inference.py`
- Artifacts stored in `artifacts/`

Recommended MLOps lifecycle:

1. **Data**
   - Source from `posts` table (`title + content`).
   - Validate schema and text quality (empty/null filtering).
2. **Training pipeline**
   - Scheduled job (daily/weekly) in CI or orchestrator.
   - Save artifacts versioned by model/date (`s3://.../models/reco/v1/...`).
3. **Model registry**
   - Track model metadata (version, train date, dataset hash, metrics).
4. **Validation gate**
   - Offline metric checks (precision@k, coverage).
   - Promote only if metrics pass threshold.
5. **Deployment**
   - Load latest approved model artifact on app startup (or sidecar model server).
6. **Monitoring**
   - Track CTR for recommended articles, drift in content features, fallback rate.
7. **Rollback**
   - Keep N-1 model active for immediate rollback.

## 6) Release safety checks

```bash
./scripts/release_check.sh
```

## 7) Suggested next upgrades

- Add Alembic migrations and run in CI before deploy.
- Add pytest integration tests for auth, CRUD, and analytics.
- Add rate limiting for tracking endpoints.
- Add Redis caching for popular pages and analytics aggregates.
- Add Terraform/IaC for environment provisioning.
