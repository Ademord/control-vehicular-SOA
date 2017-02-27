kubectl delete deployment camaras && docker build -t ademord/camara:latest ./app && docker push ademord/camara:latest && kubectl create -f deployment.json
sleep(2)
kubectl describe service propietarios | grep Ingress && kubectl get all | grep propietarios
