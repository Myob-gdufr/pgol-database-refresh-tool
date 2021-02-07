
# pgol-database-refresh-tool
The code and deployment for the pgol-database-refresh-tool

Implementation of [PGDEV-4288 Update Test Database Refresh Tool Solution Proposal](https://myobconfluence.atlassian.net/wiki/spaces/PGDEV/pages/2010678619/PGDEV-4288+Update+Test+Database+Refresh+Tool+Solution+Proposal)

Code conventions follow similar structure to the [pgol-lambda-sql](https://github.com/MYOB-Technology/pgol-lambda-sql) repo

deploy pipeline:
`../pgol-cf-bootstrap/src/cf-bootstrap.ps1 etc/bootstrapper/settings_pipeline_build.json`

deploy destination account assets to test:
`../pgol-cf-bootstrap/src/cf-bootstrap.ps1 .\etc\bootstrapper\settings_account_assets_test.json`
