

docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg14-latest

# If you want to access the container from the host but avoid exposing it to the outside world, you can bind to 127.0.0.1 instead of the public interface, using this command:
docker run -d --name timescaledb -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb-ha:pg14-latest

# If you don't want to install psql and other PostgreSQL client tools locally, we can use the version of psql that is bundled within the container with this command:
docker exec -it timescaledb psql -U postgres

vim /var/lib/postgresql/data/postgresql.conf

