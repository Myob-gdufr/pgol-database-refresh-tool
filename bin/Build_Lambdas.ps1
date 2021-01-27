#!/usr/local/bin/pwsh
sam build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
