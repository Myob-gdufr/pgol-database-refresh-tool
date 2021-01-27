<#
.NOTES
    Version: 0.4.0.2

#>


###################################################################################################
#                                                                                                 #
#  Get-LogLevelAsInteger                                                                          #
#                                                                                                 #
#                                                                                                 #
###################################################################################################
function Get-LogLevelAsInteger(
 [Parameter(Mandatory=$true)][ValidateSet("FAIL","ERROR","WARN", "NOTICE", "INFO", "DEBUG", "TRACE")][String] $LogLevel
) {
  switch($LogLevel)
  {
    "TRACE" { 1 }
    "DEBUG" { 2 }
    "INFO" { 3 }
    "NOTICE" { 4 }
    "WARN" { 5 }
    "ERROR" { 6 }
    "FAIL" { 7 }
  }
}

###################################################################################################
#                                                                                                 #
#  Get-LogLevelAsString                                                                           #
#                                                                                                 #
#                                                                                                 #
###################################################################################################
function Get-LogLevelAsString(
 [Parameter(Mandatory=$true)][ValidateSet(1,2,3, 4, 5, 6, 7)][Integer] $LogLevel
) {
  switch($LogLevel)
  {
    1 { "TRACE" }
    2 { "DEBUG" }
    3 { "INFO" }
    4 { "NOTICE" }
    5 { "WARN" }
    6 { "ERROR" }
    7 { "FAIL" }
  }
}

###################################################################################################
#                                                                                                 #
#  Get-LogLevelColour                                                                             #
#                                                                                                 #
#                                                                                                 #
###################################################################################################
function Get-LogLevelColour
{
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory=$true)][ValidateSet(1,2,3,4,5,6,7)][Int32] $LogLevelNumber
    )
    PROCESS {
        switch($LogLevelNumber)
        {
            1 { "DarkGray" }
            2 { "Gray" }
            3 { "White" }
            4 { "Cyan" }
            5 { "Yellow" }
            6 { "Red" }
            7 { "Red" }
        }
    }
}


###################################################################################################
#                                                                                                 #
#  Set-LogLevel                                                                                   #
#                                                                                                 #
#  Sets the log level.  All log messages at, or above this severity will now be logged.           #
#                                                                                                 #
###################################################################################################
function Set-LogLevel(
 [Parameter(Mandatory=$true)][ValidateSet("FAIL","ERROR","WARN", "NOTICE", "INFO", "DEBUG", "TRACE")][String] $LogLevel,
 [Switch] $Initialize
) {
  $NewLogLevelInteger = Get-LogLevelAsInteger -LogLevel $LogLevel
  if ($Initialize -or ($Global:LogLevel -ne $NewLogLevelInteger)) {
    Set-Variable -Name "LogLevelInteger" -Value $NewLogLevelInteger -Scope Global
    #  Change in configuration, so needs to be logged.
    New-LogEntry -level INFO "LOG001" "The setting for logLevel='$LogLevel'."
  }
}

###################################################################################################
#                                                                                                 #
#  Fail  - A message logged at level fail is very serious. Not only has something not worked,     #
#          It has left the server in a state that could not be recovered from automatically and   #
#          it will either require a server rotation, or manual intervention to fix the server.    #
#                                                                                                 #
###################################################################################################
function LogFail(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "FAIL" -Event $Event -Message $Message
}

###################################################################################################
#                                                                                                 #
# Error - A message logged at level error is a serious event. A failure has occured that is not   #
#         an expected failure.  These errors should be investigated to understand the root cause, #
#         with recomendations documented for mitigation and prevention.                           #
#                                                                                                 #
###################################################################################################
function LogError(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "ERROR" -Event $Event -Message $Message
}


###################################################################################################
#                                                                                                 #
# Warn  - A message logged at level warn is a predictable, but serious failure. A failure has     #
#         occured such as a configuration error, or a remote service is unavailable. These        #
#         Messages at this level mean that something is misconfigured or there is a significant   #
#         failure in another part of the environment, that has persisted longer than the normal   #
#         recovery time.                                                                          #
#                                                                                                 #
###################################################################################################
function LogWarn(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "WARN" -Event $Event -Message $Message
}


###################################################################################################
#                                                                                                 #
# Notice - A message logged at level notice is information that is important to the monitoring of #
#          the environment.  Examples could include reporting of, or change in environmental      #
#          settings, the starting and stopping of services and information on transaction rates.  #
#          Transaction rates should be logged no more frequently than at the rate of 1/minute per #
#          process.                                                                               #
#                                                                                                 #
#          If remote service fails to respond, and we are retrying, then we should log at this    #
#          level.                                                                                 #
#                                                                                                 #
###################################################################################################
function LogNotice(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "NOTICE" -Event $Event -Message $Message
}


###################################################################################################
#                                                                                                 #
# Info  - A message logged at level info is information about the performance of a transaction    #
#         that is of general interest. It will typically include start and end of all of the      #
#         transactions and include duration, key properties of the transaction and whether it     #
#         completed successfully.                                                                 #
#                                                                                                 #
#         A transaction that failed because of the request contained invalid data would log the   #
#         detection of the invalid data at info level, and the client should log that it has also #
#         received the invalid request response                                                   #
#                                                                                                 #
###################################################################################################
function LogInfo(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "INFO" -Event $Event -Message $Message
}

###################################################################################################
#                                                                                                 #
# Debug - A message logged at level debug is typically positive confirmation that key steps in a  #
#         process have occured. All connections to remote services should be logged this way,     #
#         including information about the current transaction id, duration, parameters and idents #
#         for the key objects involved.                                                           #
#                                                                                                 #
###################################################################################################
function LogDebug(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "DEBUG" -Event $Event -Message $Message
}


###################################################################################################
#                                                                                                 #
# Trace - A message should be logged at trace level every time:                                   #
#         - around a loop including the range of values being iterated logged as a single message #
#         - logical branching decision including the outcome of the decision                      #
#         - values at entry / exit of all non trivial functions
#                                                                                                 #
###################################################################################################
function LogTrace(
  [Parameter(Mandatory=$True,Position=1)][String] $Event,
  [Parameter(Mandatory=$True,Position=2)][String] $Message
) {
  New-LogEntry -Level "TRACE" -Event $Event -Message $Message
}

###################################################################################################
#                                                                                                 #
#  Log                                                                                            #
#                                                                                                 #
#  Write a log entry to disk and console, if its log level is equal or above the logging level.   #
#                                                                                                 #
###################################################################################################
function New-LogEntry(
  [ValidateSet("FAIL","ERROR","WARN", "NOTICE", "INFO", "DEBUG", "TRACE")][String] $Level = "INFO",
  [String] $Event,
  [String] $Message
) {
  $LevelInteger = Get-LogLevelAsInteger $Level
  if (!(Test-Path variable:global:LogLevelInteger) -or  ($LevelInteger -ge $Global:LogLevelInteger)) {
      $Colour = Get-LogLevelColour $LevelInteger
      Write-Host -ForegroundColor $Colour "$Level|$Event|$Message"
  }
}


###################################################################################################
#                                                                                                 #
#  LogErrorRecord                                                                                 #
#                                                                                                 #
#  Specialised logger for ErrorRecords that split the error into seperate log messages to assist  #
#  with debugging the error.                                                                      #
#                                                                                                 #
###################################################################################################
function New-ErrorRecordLogEntry(
  [Parameter(Mandatory=$True)][System.Management.Automation.ErrorRecord] $ErrorRecord,
  [ValidateSet("FAIL","ERROR","WARN", "NOTICE", "INFO", "DEBUG", "TRACE")][String] $Level = "DEBUG"
) {
    # $ErrorRecord | Format-Table
    $HistoryID = $ErrorRecord.InvocationInfo.HistoryId
    $LineText = $ErrorRecord.InvocationInfo.Line -replace "`n"
    $LineNo = $ErrorRecord.InvocationInfo.ScriptLineNumber
    $Source = $ErrorRecord.InvocationInfo.ScriptName

    $Activity = $ErrorRecord.CategoryInfo.Activity
    $Category = $ErrorRecord.CategoryInfo.Category
    $Reason = $ErrorRecord.CategoryInfo.Reason

    New-LogEntry -Level $Level  -Event "EXPS00" -Message "When performing activity=`"$Activity`" an error=`"$Category`" occured of errorReason=`"$Reason`" at line=`"$LineNo`" in powershellScript=`"$Source`".  The error occured on the scriptText=`"$LineText`" and is assigned errorEventId=`"$HistoryID`"."

    $Ex = $ErrorRecord.Exception
    $FormattedStackTrace = $ErrorRecord.ScriptStackTrace -Replace [System.Environment]::NewLine, " <<< "
    New-LogEntry -Level Warn -Event "EXPSXX" -Message "StackTrace for errorEventId=`"$HistoryID`": $FormattedStackTrace"
    $Nested = 0
    while($null -ne $Ex)
    {
      $ExType=$Ex.pstypenames[0]
      $ExMesssage=$Ex.Message

      New-LogEntry -Level $Level -Event "EXPS01" -Message "The errorEventId=`"$HistoryID`" seq=`"$Nested`" is type=`"$ExType`" with message=`"$ExMesssage`"."
      $Nested = $Nested + 1
      $Ex = $Ex.InnerException
    }
}

