################################################################################
#
#			FOR DEVELOPMENT
#
################################################################################

build: clean
	docker-compose build

run-local: clean
	docker-compose up -d
	docker-compose logs -f -t

clean:
	docker-compose down
	rm -rf *.pyc
	rm -rf celerybeat*
