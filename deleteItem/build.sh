aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 767397954312.dkr.ecr.us-east-1.amazonaws.com

docker build -t delete_item_repo .

docker tag delete_item_repo:latest 767397954312.dkr.ecr.us-east-1.amazonaws.com/delete_item_repo:latest

docker push 767397954312.dkr.ecr.us-east-1.amazonaws.com/delete_item_repo:latest

aws lambda update-function-code --function-name deleteItem --image-uri 767397954312.dkr.ecr.us-east-1.amazonaws.com/delete_item_repo:latest