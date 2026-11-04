param([string]$Device='cuda',[string]$SafeMode='gru-native',[string]$PythonExe='',[switch]$Smoke)
$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root
. .\FINAL_E2E_C23_POWERSHELL_COMMON.ps1
Initialize-FinalE2EC23Python -PythonExe $PythonExe
Assert-PassJson 'outputs\final_e2e_c23_external_d2904_t2904\preflight\external_baseline_identity.json'
$ArgsList=@('tools/prepare_final_e2e_c23_external_sources.py',"--device=$Device","--safe_mode=$SafeMode")
if($Smoke){$ArgsList+='--smoke'}
$Log='outputs\final_e2e_c23_external_d2904_t2904\logs\external_source_assets.log'
$rc=Invoke-FinalPython -Arguments $ArgsList -Log $Log
if($rc -ne 0){throw "External source assets failed exit=$rc"}
Assert-PassJson 'outputs\final_e2e_c23_external_d2904_t2904\source_assets\source_assets_manifest.json'
Write-Host '[External] Source assets PASS'
