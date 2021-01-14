# pgol-dataset-s3-service
The code and deployment pgol-dataset-s3-service

Implemenation of https://myobconfluence.atlassian.net/wiki/spaces/PGOS/pages/1775535752/Dataset+File+Service+Solution+Proposal+-+S3+Buckets


File structure:
    Naming conventions: 
        Since the operations are completed sequentially:
            1. create all necessary aws resources (including pipeline)
            2. create all necessary functions (primarily lambdas), etc
        the names are prefixed with the sequence number 