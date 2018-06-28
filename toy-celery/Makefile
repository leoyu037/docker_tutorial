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

install:
	# python setup.py install
	pip install -e .

clean:
	docker-compose down
	rm -rf *.pyc
	rm -rf celerybeat*
