#!/usr/local/bin/pwsh
sam build --template-file "etc/sam/template.yml" --base-dir .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
