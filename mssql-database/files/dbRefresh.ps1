#Import-Module PureStorageDbaTools

#Get-DbaDatabase -sqlinstance z-stn-win2016-a\devopsprd -Database tpch-no-compression

Invoke-Command -ComputerName z-stn-win2016-a -ScriptBlock { Write-Host "Test" }
