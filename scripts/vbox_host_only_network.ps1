# See http://msdn2.microsoft.com/en-us/library/bb201634.aspx
#
# *NdisDeviceType
#
# The type of the device. The default value is zero, which indicates a standard
# networking device that connects to a network.
#
# Set *NdisDeviceType to NDIS_DEVICE_TYPE_ENDPOINT (1) if this device is an
# endpoint device and is not a true network interface that connects to a network.
# For example, you must specify NDIS_DEVICE_TYPE_ENDPOINT for devices such as
# smart phones that use a networking infrastructure to communicate to the local
# computer system but do not provide connectivity to an external network.
#
# Usage: Run in an elevated shell (Vista/7) or as Adminstrator (XP/2003).
#
# PS> .\Edit-VirtualBoxAdapters.ps1

# Boilerplate Elevation Check

$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal $identity
$elevated = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $elevated) {
    $error = "Sorry, you need to run this script"
    if ([System.Environment]::OSVersion.Version.Major -gt 5) {
        $error += " in an elevated shell."
    } else {
        $error += " as Administrator."
    }
    throw $error
}

# Key in Registry containing all Network Adapters
pushd 'HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}'

# Find all VirtualBox adapters and update them accordingly (Ignore and continue on error)
dir -ea 0  | % {
    $node = $_.pspath
    $desc = gp $node -name driverdesc
    if ($desc -like "*virtualbox host-only*") {
        Write-Host ("Found adapter: {0} " -f $desc.driverdesc)
        if ($host.ui.PromptForChoice("Continue", "Process adapter?", [Management.Automation.Host.ChoiceDescription[]]@("&No", "&Yes"), 0) -eq $true) {
            Set-ItemProperty $node -Name "*NdisDeviceType" -Value 1 -Type "DWORD"
        }
    }
}
popd

# Disable and re-enable all VirtualBox network adapters to enforce new setting
gwmi win32_networkadapter | ? {$_.name -like "*virtualbox host-only*" } | % {

    # Disable
    Write-Host -nonew "Disabling $($_.name) ... "
    $result = $_.Disable()
    if ($result.ReturnValue -eq -0) { Write-Host " success." } else { Write-Host " failed." }

    # Enable
    Write-Host -nonew "Enabling $($_.name) ... "
    $result = $_.Enable()
    if ($result.ReturnValue -eq -0) { Write-Host " success." } else { Write-Host " failed." }
}
