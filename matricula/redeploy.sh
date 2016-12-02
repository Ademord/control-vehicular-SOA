kubectl delete deployment matriculas && docker build -t ademord/matricula:latest ./app && docker push ademord/matricula:latest && kubectl create -f deployment.json
kubectl describe service matriculas | grep Ingress && kubectl get all | grep matriculas

