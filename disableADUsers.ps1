<#
-------------------Automated User Account Cleanup-------------------
This script Retrieve all inactive Active Directory users (users not logged in for the past 90 days)
Disable the inactive users.
Export a report of disabled users to inactive_users.csv

Notes:
    - Use an App Password instead of your regular Gmail password.
    - App Password can be generated from your Google Account's security settings.
    - Log File Path: C:\Users\Laptop\PycharmProjects\pythonProject1\SystemAlert.log

-------------------NotTested-------------------
#>

# Import AD module
Import-Module ActiveDirectory

# Define parameters
$DaysInactive = 90
$Time = (Get-Date).AddDays(-$DaysInactive)
$ExportPath = "C:\inactive_users.csv"

# Find inactive users
$InactiveUsers = Get-ADUser -Filter {LastLogonDate -lt $Time -and Enabled -eq $true} -Properties LastLogonDate

# Disable inactive users
foreach ($user in $InactiveUsers) {
    Disable-ADAccount -Identity $user.SamAccountName
    Write-Output "Disabled user: $($user.SamAccountName)"
}

# Export report
$InactiveUsers | Select-Object Name, SamAccountName, LastLogonDate | Export-Csv -Path $ExportPath -NoTypeInformation

Write-Output "Inactive user report saved to $ExportPath"
