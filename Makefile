db:
	docker-compose run --rm web python manage.py migrate

run:
	docker-compose up 

shell:
	docker-compose run --rm web python manage.py shell 

test:
	docker-compose  run --rm  web python manage.py test