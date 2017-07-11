kubectl delete deployment coincidencias 
docker build -t ademord/coincidencia:latest ./app && docker push ademord/coincidencia:latest && kubectl create -f deployment.json
kubectl describe service coincidencias | grep Ingress && kubectl get all | grep coincidencias
