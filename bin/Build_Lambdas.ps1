#!/usr/local/bin/pwsh
sam build --template-file "sam-template.yml"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
