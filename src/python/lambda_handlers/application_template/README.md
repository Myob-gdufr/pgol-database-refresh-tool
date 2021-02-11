
# application template
The template code for lambda serverless applications. 
It has three main parts:
    lambda_handler:
        sanitize inputs
        make calls to support modules (mainly for aws interactions)
        all success and failure code paths must provide a response to the caller
        example file: lambda_function.py
    support modules:
        mainly provide aws interaction functions using boto3 library
        current example files: application_template.py, get_secret.py
    Dockerfile:
        enables building the image with all required libraries for deployment to AWS ECR
        example file: Dockerfile

# Deployment:
############################################################
# build the app using docker
############################################################
# build the docker image from lambda_handler root directory (e.g. src/python/lambda_handlers/rds_get_databases)
cd pgol-database-refresh-tool/src/python/lambda_handlers/application_template
# the docker build looks to the Dockerfile in the current directory for build instructions 
# the tag ":application_template" helps with consistency and clarity 
docker build -t pgol/database_refresh_tool:application_template .

# IF you want to test it locally: run the image and load up a bash shell inside it
docker run -it pgol/database_refresh_tool:application_template /bin/bash

############################################################
# Push the image to ECR
############################################################
# PROD only, see other accounts below
# log in to ECR
aws ecr get-login-password --region ap-southeast-2 --profile prod | docker login --username AWS --password-stdin 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com

# tag the image for pushing up to AWS ECR
docker tag pgol/database_refresh_tool:application_template 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:application_template

# push the image to ECR
docker push 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:application_template

# now the image can be used to deploy a lambda using the image URI@digest
# 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool@sha256:126f810048fa221abed19668b03e4a52b2683b551bd77bd1778a51a8117b869b

############################################################
# TEST only, see other accounts below

# log in to ECR
aws ecr get-login-password --region ap-southeast-2 --profile test | docker login --username AWS --password-stdin 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com

# tag the image for pushing up to AWS ECR
docker tag pgol/database_refresh_tool:application_template 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:application_template

# push the image to ECR
docker push 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:application_template

# now the image can be used to deploy a lambda using the image URI@digest, the interface in the aws management console is super simple
# 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool@sha256:126f810048fa221abed19668b03e4a52b2683b551bd77bd1778a51a8117b869b
