aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 767397954312.dkr.ecr.us-east-1.amazonaws.com

docker build -t pull_ebay_data_repo .

docker tag pull_ebay_data_repo:latest 767397954312.dkr.ecr.us-east-1.amazonaws.com/pull_ebay_data_repo:latest

docker push 767397954312.dkr.ecr.us-east-1.amazonaws.com/pull_ebay_data_repo:latest

aws lambda update-function-code --function-name pullEbayData --image-uri 767397954312.dkr.ecr.us-east-1.amazonaws.com/pull_ebay_data_repo:latest