kubectl delete deployment recolector && docker build -t ademord/recolector:latest ./app && docker push ademord/recolector:latest && kubectl create -f deployment.json

