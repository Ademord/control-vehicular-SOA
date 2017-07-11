FROM postgres
ENV POSTGRES_USER=homestead
ENV POSTGRES_DB=homestead
ENV POSTGRES_PASSWORD=secret
COPY db /docker-entrypoint-initdb.d/
COPY init.sh /docker-entrypoint-initdb.d/
# CMD psql homestead < db -U homestead
