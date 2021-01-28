#!/usr/local/bin/pwsh
sam build --template-file "etc/sam/template.yml"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
