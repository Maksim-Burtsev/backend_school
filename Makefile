db:
	docker-compose run web python manage.py migrate

run:
	docker-compose up 

shell:
	docker-compose run web python manage.py shell 