#!/usr/local/bin/pwsh
try {
    Invoke-Expression "${PSScriptRoot}/../Prepare_Lambda_Deploy.ps1"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
catch {
    Write-Output $_.Exception.Message
    exit 1
}
