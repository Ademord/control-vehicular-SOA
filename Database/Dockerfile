FROM postgres
ENV POSTGRES_USER=homestead
ENV POSTGRES_DB=homestead
ENV POSTGRES_PASSWORD=secret
ADD db.sql db.sql
CMD pg_restore -d homestead db.sql -U homestead
