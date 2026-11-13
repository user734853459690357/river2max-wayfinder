# Keeps Windows from idle-sleeping while this process runs (display may still turn off).
# Changes no power settings; sleep returns to normal when the window is closed / process ends.
param([int]$Hours = 8)
Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
$ES_CONTINUOUS = [uint32]"0x80000000"; $ES_SYSTEM_REQUIRED = [uint32]"0x00000001"
[void][Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED)
Write-Host "Keeping system awake for $Hours h (Ctrl+C to stop)..."
Start-Sleep -Seconds ($Hours * 3600)
