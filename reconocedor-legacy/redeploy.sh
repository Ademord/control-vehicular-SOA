kubectl delete deployment reconocedor 
docker build -t ademord/reconocedor:latest ./app && docker push ademord/reconocedor:latest && kubectl create -f deployment.json
