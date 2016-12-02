kubectl delete deployment coincidencias 
docker build -t ademord/coincidencia:latest ./app && docker push ademord/coincidencia:latest && kubectl create -f deployment.json

