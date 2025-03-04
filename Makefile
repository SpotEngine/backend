production: 
	docker compose up -d --build --remove-orphans

create-db:
	docker compose up -d --build app-db 
	docker exec -it app-db psql -U postgres -c "create database app;"
	docker exec -it app-db psql -U postgres -c "create user app with encrypted password 'app';"
	docker exec -it app-db psql -U postgres -c "grant all privileges on database app to app;"
	docker exec -it app-db psql -U postgres -c "ALTER DATABASE app OWNER TO app;"
	docker exec -it app-db psql -U postgres -c "ALTER USER app CREATEDB;"
	docker exec -it app-db psql -U postgres -c "\connect app \x \\GRANT CREATE ON SCHEMA public TO app;"
db:
	docker compose up -d app-db 

dev:
	docker compose up -d --build --remove-orphans zoo1 kafka1 web nginx spot && docker compose logs -f -n 5 

dev-web:
	docker compose up -d --build --remove-orphans app-web && docker logs -f -n 5 app-web

test:
	docker compose up -d --build --remove-orphans app-web && docker exec -it app-web python manage.py test

infra:
	# make clean
	docker compose up -d --build --remove-orphans app-db app-redis kafka1 zoo1
	
shell:
	docker compose up -d --build --remove-orphans app-web && docker exec -it app-web python manage.py shell

stop:
	docker compose down


clean:
	docker stop $(docker ps -q)

