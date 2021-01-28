#!/usr/local/bin/pwsh
try {
    $SamConfigName = "samconfig-prod.toml"
    $DeployRole = "arn:aws:iam::574138626371:role/DatasetS3Service-Deployment"
    $VpcId = "vpc-4da00628"
    $VpcName = "PayGlobalOnline"

    Invoke-Expression "${PSScriptRoot}/../Deploy_Lambdas.ps1 -SamConfigFileName ${SamConfigName} -DeploymentRoleArn ${DeployRole} -VpcId ${VpcId} -VpcName ${VpcName}"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
catch {
    Write-Output $_.Exception.Message
    exit 1
}


