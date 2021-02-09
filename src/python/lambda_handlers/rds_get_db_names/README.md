
# pgol-database-refresh-tool
The code and deployment for the rds_get_db_names lambda

# Usage:

# build the docker image from lambda_handler root directory (e.g. src/python/lambda_handlers/rds_get_databases)
cd pgol-database-refresh-tool/src/python/lambda_handlers/rds_get_db_names
# the docker build looks to the Dockerfile in the current directory for build instructions 
# the local tag doesn't really matter except for consistency
docker build -t pgol/database_refresh_tool:rds_get_db_names .

# run the image and load up a shell connection if you want to test local execution
docker run -it pgol/database_refresh_tool:rds_get_db_names /bin/bash

# tag the image for pushing up to AWS ECR
docker tag pgol/database_refresh_tool:rds_get_db_names 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:rds_get_db_names

# push the imag to ECR
docker push 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool:rds_get_db_names

# now the image can be used to deploy a lambda using the image URI@digest
# 574138626371.dkr.ecr.ap-southeast-2.amazonaws.com/pgol/database_refresh_tool@sha256:126f810048fa221abed19668b03e4a52b2683b551bd77bd1778a51a8117b869b

