network:
	@if [ $(shell docker network ls -q --filter name=kube-lab | wc -l) -eq 0 ]; then docker network create kube-lab; fi

start: network
	@docker compose -f docker-compose.yml up -d --build

test: network
	@docker compose -f docker-compose.tests.yml -f docker-compose.yml up -d 

stop:
	@docker compose -f docker-compose.yml down

status:
	@docker compose -f docker-compose.yml ps

logs:
	@docker compose logs -f

clean:
	@sudo rm -rf .k3s-agent/ .k3s-server/ .kubeconfig/

restart:
	@make stop start
