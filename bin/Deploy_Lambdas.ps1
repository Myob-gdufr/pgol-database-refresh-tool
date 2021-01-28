[CmdletBinding()]
param(
    [parameter(Mandatory=$true)][String]$SamConfigFileName=$null,
    [parameter(Mandatory=$true)][String]$DeploymentRoleArn=$null,
    [parameter(Mandatory=$true)][String]$PythonLambdaServiceRoleArn=$null,
    [parameter(Mandatory=$true)][String]$VpcName=$null,
    [String]$LogLevel= $Env:LogLevel
)

$RootPath = $PSScriptRoot.substring(0,$PSScriptRoot.Length - 4)

# Imports
. "${RootPath}/bin/include/Log.ps1"

if ($LogLevel -eq $null)
{
    $LogLevel = "INFO"
}

try {
    Set-LogLevel -LogLevel $LogLevel -Initialize

    New-LogEntry -level INFO -Event "BLD???" -Message "Attempting to assume deployment role in destination account"
    $RoleSessionName = "TimeSeriesBackupPipeline-" + [Guid]::NewGuid().ToString()
    $Credentials = (Use-STSRole -RoleArn "$DeploymentRoleArn" -RoleSessionName "$RoleSessionName").Credentials 
    Set-AWSCredential -StoreAs "assumed_profile" -AccessKey $Credentials.AccessKeyId -SecretKey $Credentials.SecretAccessKey -SessionToken $Credentials.SessionToken
    # Set-AWSCredential is a powershell cmdlet, sans exit-code ...
    if ($? -eq $false) {
        New-LogEntry -level WARN -Event "BLD9??" -Message "Failed to set AWS Credentials into temporary profile"
        exit 1
    }
    New-LogEntry -level NOTICE -Event "BLD???" -Message "Created temporary profile with cross account credentials"

    New-LogEntry -level INFO -Event "BLD???" -Message "Calculating Security Context"
    $vpc_filter =  @{Name = "tag:VPC"; Values="$VpcName" }
    $python_role_filter = @{Name = "tag:Role"; Values = "PythonLambdas" }
    $subnet_access_filter = @{Name = "tag:Role"; Values = "Nat"}

    $python_security_group_id = (Get-EC2SecurityGroup -Filter @($vpc_filter; $python_role_filter)  -Select "SecurityGroups.GroupId" -ProfileName "assumed_profile")
    if ($? -eq $false) {
        New-LogEntry -level WARN -Event "BLD9??" -Message "Failed to identify python security group for deplopyment."
        exit 1
    }

    $subnet_ids = (Get-EC2Subnet -Filter $($vpc_filter; $subnet_access_filter) -Select "Subnets.SubnetId" -ProfileName "assumed_profile")
    if ($? -eq $false) {
        New-LogEntry -level WARN -Event "BLD9??" -Message "Failed to identify subnet ids for deployment"
        exit 1
    }
    $subnet_ids = $subnet_ids -Join ',' # Convert String[] to comma separated string

    New-LogEntry -level NOTICE -Event "BLD???" -Message "Starting the deploy process"
    sam deploy `
        --config-file $SamConfigFileName `
        --profile assumed_profile `
        --no-confirm-changeset `
        --parameter-overrides " `
            VpcName=$VpcName `
            PythonLambdaServiceRoleArnParam=$PythonLambdaServiceRoleArn `
            PythonLambdaSecurityGroupIdParam=$python_security_group_id `
            VpcSubnetIdsParam=$subnet_ids"
    if ($LASTEXITCODE -ne 0) {
        New-LogEntry -level WARN -Event "BLD9??" -Message "The SAM deploy command returned a failure code."
        exit $LASTEXITCODE
    }
}
catch {
    New-ErrorRecordLogEntry -ErrorRecord $PSItem -level Warn
    New-LogEntry -level ERROR -Event "SWT003" -Message "The task='$Task' that ran process='$ScriptName' using transactionId='$TransactionId' failed to complete successfully."
    exit 1
}
