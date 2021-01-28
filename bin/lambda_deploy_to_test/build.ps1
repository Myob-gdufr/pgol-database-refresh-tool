#!/usr/local/bin/pwsh
try {
    $SamConfigName = "samconfig-test.toml"
    $DeployRole = "arn:aws:iam::263800988620:role/DatasetS3Service-Deployment"
    $VpcId = "vpc-9e05b7fa"
    $VpcName = "Test-PayGlobalOnline"

    Invoke-Expression "${PSScriptRoot}/../Deploy_Lambdas.ps1 -SamConfigFileName ${SamConfigName} -DeploymentRoleArn ${DeployRole} -VpcId ${VpcId} -VpcName ${VpcName}"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
catch {
    Write-Output $_.Exception.Message
    exit 1
}
