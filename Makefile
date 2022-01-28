.PHONY: startdocker
startdocker:
	docker-compose up -d --no-recreate

.PHONY: stopdocker
stopdocker:
	docker-compose down