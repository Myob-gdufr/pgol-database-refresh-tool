#!/usr/local/bin/pwsh
try {
    $SamConfigName = "etc/sam/samconfig-prod.toml"
    $DeployRole = "arn:aws:iam::574138626371:role/DatasetS3Service-Deployment"
    $PythonRole = "arn:aws:iam::574138626371:role/DatasetS3-PythonLambdaServiceRole"
    $VpcName = "PayGlobalOnline"

    Invoke-Expression "${PSScriptRoot}/../Deploy_Lambdas.ps1 -SamConfigFileName ${SamConfigName} -DeploymentRoleArn ${DeployRole} -PythonLambdaServiceRoleArn ${PythonRole} -VpcName ${VpcName}"      
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
catch {
    Write-Output $_.Exception.Message
    exit 1
}


