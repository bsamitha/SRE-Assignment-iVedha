<#
-------------------System Health Check-------------------

#Requires -Version 5.1

This script check the following system parameters on a Windows server:
    - CPU usage
    - Memory usage
    - Disk space availability
If any metric crosses 80% utilization, log the event and send an alert email.

Email Settings:
    - SMTP Server   : smtp.gmail.com
    - Port          : 587 (TLS)

Notes:
    - Use an App Password instead of your regular Gmail password.
    - App Password can be generated from your Google Account's security settings.
    - Log File Path: C:\Users\Laptop\PycharmProjects\pythonProject1\SystemAlert.log

-------------------DeveloperTested-------------------
#>

$smtpServer = "smtp.gmail.com"
$smtpPort = 587
$to = "basnayake92@gmail.com"
$from = "basnayakemsl@gmail.com"
$subject = "High System Utilization Alert"
$logFile = "C:\Users\Laptop\PycharmProjects\pythonProject1\SystemAlert.log"

#Authentication
#Gmail account email and App Password
$smtpUser = "basnayakemsl@gmail.com"
$appPassword = ""  # Use your 16-char app password
$securePassword = ConvertTo-SecureString $appPassword -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential ($smtpUser, $securePassword)

# CPU usage
$cpuUsage = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
$cpuUsage = [math]::Round($cpuUsage, 2)
Write-Output "CPU Usage: $cpuUsage%"

# Memory usage
$os = Get-CimInstance Win32_OperatingSystem
$totalMemory = $os.TotalVisibleMemorySize
$freeMemory = $os.FreePhysicalMemory
$usedMemoryPercent = [math]::Round((($totalMemory - $freeMemory) / $totalMemory) * 100, 2)
Write-Output "Memory Usage: $usedMemoryPercent%"

# Disk usage
$diskUsage = @()
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    $used = ($_.Size - $_.FreeSpace)
    $percentUsed = [math]::Round(($used / $_.Size) * 100, 2)
    Write-Output "Disk $($_.DeviceID) Usage: $percentUsed%"
    $diskUsage += [PSCustomObject]@{
        DeviceID = $_.DeviceID
        UsedPercent = $percentUsed
    }
}

# Function to log and email alerts
function Send-Alert {
    param (
        [string]$metric,
        [string]$value
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $message = "$timestamp ALERT: $metric is at $value% utilization."

    # Log the event
    Add-Content -Path $logFile -Value $message

    # Send email
    Send-MailMessage -From $from -To $to -Subject $subject -Body $message `
        -SmtpServer $smtpServer -Port $smtpPort -Credential $credential `
        -UseSsl

    Write-Output $message
}

# Check CPU
if ($cpuUsage -gt 80) {
    Send-Alert -metric "CPU Usage" -value $cpuUsage
}

# Check Memory
if ($usedMemoryPercent -gt 70) {
    Send-Alert -metric "Memory Usage" -value $usedMemoryPercent
}

# Check Disks
foreach ($disk in $diskUsage) {
    if ($disk.UsedPercent -gt 70) {
        Send-Alert -metric "Disk $($disk.DeviceID)" -value $disk.UsedPercent
    }
}

Write-Output "Health check completed."
