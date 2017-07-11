kubectl delete deployment propietarios
docker build -t ademord/propietario:latest ./app && docker push ademord/propietario:latest && kubectl create -f deployment.json && kubectl describe service propietarios | grep Ingress && kubectl get all | grep propietarios

