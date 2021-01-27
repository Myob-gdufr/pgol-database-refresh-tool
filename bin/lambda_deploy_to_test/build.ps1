#!/usr/local/bin/pwsh
try {
    $SamConfigName = "samconfig-test.toml"
    $DeployRole = "arn:aws:iam::263800988620:role/TimeSeriesBackup-Deployment"
    $DotNetRole = "arn:aws:iam::263800988620:role/TimeSeriesBackup-DotNetLambdaServiceRole"
    $PythonRole = "arn:aws:iam::263800988620:role/TimeSeriesBackup-PythonLambdaServiceRole"
    $VpcName = "Test-PayGlobalOnline"

    Invoke-Expression "${PSScriptRoot}/../Deploy_Lambdas.ps1 -SamConfigFileName ${SamConfigName} -DeploymentRoleArn ${DeployRole} -DotNetLambdaServiceRoleArn ${DotNetRole}  -PythonLambdaServiceRoleArn ${PythonRole} -VpcName ${VpcName}"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
catch {
    Write-Output $_.Exception.Message
    exit 1
}
