FROM python:3-onbuild
ENV DATABASE_HOST=homestead
ENV DATABASE_NAME=homestead
ENV DATABASE_USER=homestead
ENV DATABASE_PASSWORD=secret
ENV DATABASE_PORT=5432
EXPOSE 55555
ENTRYPOINT ["python","/usr/src/app/server.py"]

