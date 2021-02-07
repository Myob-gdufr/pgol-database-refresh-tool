# pgol-dataset-s3-service
The code and deployment pgol-dataset-s3-service

Implemenation of [Dataset File Service Solution Proposal - S3 Buckets](https://myobconfluence.atlassian.net/wiki/spaces/PGOS/pages/1775535752/Dataset+File+Service+Solution+Proposal+-+S3+Buckets)

Code conventions follow similar structure to the [pgol-lambda-sql](https://github.com/MYOB-Technology/pgol-lambda-sql) repo


deploy pipeline:
`../pgol-cf-bootstrap/src/cf-bootstrap.ps1 etc/bootstrapper/settings_pipeline_build.json`

deploy destination account assets to test:
`../pgol-cf-bootstrap/src/cf-bootstrap.ps1 .\etc\bootstrapper\settings_account_assets_test.json`