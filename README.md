# pgol-dataset-s3-service
The code and deployment pgol-dataset-s3-service

Implemenation of [Dataset File Service Solution Proposal - S3 Buckets](https://myobconfluence.atlassian.net/wiki/spaces/PGOS/pages/1775535752/Dataset+File+Service+Solution+Proposal+-+S3+Buckets)


Naming conventions: 
- Since the operations are completed sequentially the names are prefixed with the sequence number:
  - 1pipeline create all necessary aws resources (including pipeline)
  - 2functions all necessary functions and orchestration (lambdas, step functions), etc
