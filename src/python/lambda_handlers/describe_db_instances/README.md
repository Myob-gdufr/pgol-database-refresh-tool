
# pgol-database-refresh-tool
The code and deployment for the describe_db_instances lambda

# Deployment:

############################################################
# build the app using docker
############################################################
# build the docker image from lambda_handler root directory (e.g. src/python/lambda_handlers/rds_get_databases)
cd pgol-database-refresh-tool/src/python/lambda_handlers/describe_db_instances
# the docker build looks to the Dockerfile in the current directory for build instructions 
# the tag ":describe_db_instances" helps with consistency and clarity 
docker build -t pgol/database_refresh_tool:describe_db_instances .

# IF you want to test it locally: run the image and load up a bash shell inside it
docker run -it pgol/database_refresh_tool:describe_db_instances /bin/bash

############################################################
# Push the image to ECR
############################################################
# PROD only, see other accounts below
# log in to ECR
aws ecr get-login-password --region ap-southeast-2 --profile prod | docker login --username AWS --password-stdin 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com

# tag the image for pushing up to AWS ECR
docker tag pgol/database_refresh_tool:describe_db_instances 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:describe_db_instances

# push the image to ECR
docker push 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:describe_db_instances

# now the image can be used to deploy a lambda using the image URI@digest
# 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool@sha256:126f810048fa221abed19668b03e4a52b2683b551bd77bd1778a51a8117b869b

############################################################
# TEST only, see other accounts below

# log in to ECR
aws ecr get-login-password --region ap-southeast-2 --profile test | docker login --username AWS --password-stdin 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com

# tag the image for pushing up to AWS ECR
docker tag pgol/database_refresh_tool:describe_db_instances 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:describe_db_instances

# push the image to ECR
docker push 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:describe_db_instances

# now the image can be used to deploy a lambda using the image URI@digest, the interface in the aws management console is super simple
# 263800988620.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool@sha256:126f810048fa221abed19668b03e4a52b2683b551bd77bd1778a51a8117b869b
