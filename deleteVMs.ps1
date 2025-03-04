# List VMs older than 30 days
$cutoffDate = (Get-Date).AddDays(-30)

$oldVMs = az vm list --query "[?timeCreated<'$($cutoffDate.ToString("yyyy-MM-ddTHH:mm:ssZ"))']" -o json | ConvertFrom-Json

# Delete old VMs and save report
$report = @()
foreach ($vm in $oldVMs) {
    az vm delete --name $vm.name --resource-group $vm.resourceGroup --yes
    $report += [PSCustomObject]@{
        Name           = $vm.name
        ResourceGroup  = $vm.resourceGroup
        TimeCreated    = $vm.timeCreated
        DeletionTime   = (Get-Date)
    }
}

# Export report
$report | Export-Csv -Path "deleted_vms_report.csv" -NoTypeInformation
