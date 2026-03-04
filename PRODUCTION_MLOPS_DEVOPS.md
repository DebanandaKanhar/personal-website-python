# Production, DevOps, and MLOps Blueprint

This is an execution checklist to ship the Python app safely.

## A. DevOps path (build -> deploy -> operate)

1. **Source control**
   - Use trunk-based flow (`feature/*` -> PR -> `main`).
   - Require PR checks before merge.

2. **CI quality gates**
   - Install dependencies.
   - Run syntax/lint/tests.
   - Build Docker image.
   - Optional: dependency + container vulnerability scan.

3. **Artifact strategy**
   - Tag image as `app:<git-sha>` and `app:latest`.
   - Push to registry (GHCR/ECR/GCR).

4. **Infra environments**
   - Separate `dev`, `staging`, `prod`.
   - Separate DB instance per env.
   - Isolate secrets per env.

5. **CD rollout**
   - Auto deploy to staging after merge.
   - Smoke tests against `/healthz` and core endpoints.
   - Manual approval to production.
   - Rolling or blue/green deployment.

6. **Runtime hardening**
   - HTTPS only.
   - Secure headers at ingress/load balancer.
   - Principle of least privilege for DB and secrets.
   - Rate limit public analytics endpoint.

7. **Observability**
   - Metrics: `/metrics`.
   - Logs: JSON structured logs with request IDs.
   - Alerts: 5xx spikes, P95 latency, DB connection errors.

8. **Reliability/SRE**
   - SLOs: e.g. 99.9% uptime, P95 < 300ms.
   - Runbooks for outages.
   - Automated DB backups and restore drill.

## B. MLOps path (data -> model -> monitoring)

1. **Use case**
   - Start with article recommendation ranking.

2. **Data pipeline**
   - Collect features from `posts` and optional engagement from `page_views`.
   - Add data quality checks (null ratios, text length thresholds).

3. **Training orchestration**
   - Scheduled training (daily/weekly).
   - Script: `python -m ml.recommendation_training`.
   - Produce versioned artifacts.

4. **Model registry**
   - Record: model version, code commit, data snapshot hash, metrics.
   - Keep approval status (`candidate`, `staging`, `production`).

5. **Validation**
   - Evaluate offline metrics (precision@k/coverage/diversity).
   - Block promotion if below threshold.

6. **Deployment**
   - Load approved artifact from object storage at startup.
   - Keep fallback to previous model.

7. **Online monitoring**
   - Track CTR for recommendations.
   - Detect data drift (embedding/text distribution shift).
   - Detect model staleness (performance degradation over time).

8. **Governance**
   - Reproducibility: fixed seeds + pinned dependencies.
   - Auditability: store training logs/metadata.
   - Security: no PII in model artifacts.

## C. Suggested release milestones

1. **Milestone 1 (Week 1):** API parity + Docker + CI.
2. **Milestone 2 (Week 2):** Staging deployment + monitoring + alerts.
3. **Milestone 3 (Week 3):** Production rollout + backup/restore drill.
4. **Milestone 4 (Week 4):** MLOps pipeline automation + model registry + rollback.
