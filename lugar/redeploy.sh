kubectl delete deployment lugares
docker build -t ademord/lugar:latest ./app && docker push ademord/lugar:latest && kubectl create -f deployment.json

