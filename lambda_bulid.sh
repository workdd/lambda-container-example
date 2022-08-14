sudo service docker restart

docker build -t lambda-container-example . --no-cache

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)

docker tag lambda-container-example $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/lambda-container-example

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com

docker push $ACCOUNT_ID.dkr.ecr.us-west-2.amazonaws.com/lambda-container-example

docker rmi -f $(docker images -q)
