.PHONY: install bootstrap run docker-up train-ml release-check deploy-render

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

bootstrap:
	./scripts/bootstrap.sh

run:
	./scripts/start_local.sh

docker-up:
	./scripts/deploy_local_docker.sh

train-ml:
	python -m ml.recommendation_training

release-check:
	./scripts/release_check.sh

deploy-render:
	./scripts/deploy_render_blueprint.sh
