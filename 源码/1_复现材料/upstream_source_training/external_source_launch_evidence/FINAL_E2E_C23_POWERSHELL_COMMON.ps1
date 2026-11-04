param()
function Initialize-FinalE2EC23Python {
    param([string]$PythonExe='')
    if ($PythonExe) { $script:FinalPython=$PythonExe }
    elseif ($env:CONDA_PREFIX -and (Test-Path (Join-Path $env:CONDA_PREFIX 'python.exe'))) { $script:FinalPython=Join-Path $env:CONDA_PREFIX 'python.exe' }
    elseif (Get-Command python -ErrorAction SilentlyContinue) { $script:FinalPython=(Get-Command python).Source }
    else { throw 'Python executable not found. Pass -PythonExe.' }

    # Windows PowerShell 5.1 converts native stderr into ErrorRecord objects.
    # With ErrorActionPreference=Stop, harmless Python warnings can terminate the script.
    $oldEap=$ErrorActionPreference
    $oldNative=$null
    $hasNativePref=$false
    if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
        $hasNativePref=$true
        $oldNative=$PSNativeCommandUseErrorActionPreference
        $PSNativeCommandUseErrorActionPreference=$false
    }
    try {
        $ErrorActionPreference='Continue'
        & $script:FinalPython -c "import torch; print('Python=',__import__('sys').executable); print('torch=',torch.__version__); print('cuda=',torch.cuda.is_available()); print('gpu=',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
        $code=$LASTEXITCODE
    }
    finally {
        $ErrorActionPreference=$oldEap
        if ($hasNativePref) { $PSNativeCommandUseErrorActionPreference=$oldNative }
    }
    if ($code -ne 0) { throw "Python environment check failed exit=$code." }
}

function Invoke-FinalPython {
    param([string[]]$Arguments,[string]$Log='')
    $oldEap=$ErrorActionPreference
    $oldNative=$null
    $hasNativePref=$false
    if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
        $hasNativePref=$true
        $oldNative=$PSNativeCommandUseErrorActionPreference
        $PSNativeCommandUseErrorActionPreference=$false
    }
    try {
        # Preserve stderr in the visible log, but do not treat warnings as PowerShell failures.
        $ErrorActionPreference='Continue'
        if ($Log) {
            $parent=Split-Path $Log -Parent
            if ($parent) { New-Item -ItemType Directory -Force -Path $parent|Out-Null }
            & $script:FinalPython @Arguments 2>&1 | Tee-Object -FilePath $Log -Append | Out-Host
        }
        else {
            & $script:FinalPython @Arguments 2>&1 | Out-Host
        }
        $code=$LASTEXITCODE
    }
    finally {
        $ErrorActionPreference=$oldEap
        if ($hasNativePref) { $PSNativeCommandUseErrorActionPreference=$oldNative }
    }
    return $code
}

function Invoke-FinalPythonToFile {
    param([string[]]$Arguments,[string]$Path)
    $parent=Split-Path $Path -Parent
    if ($parent) { New-Item -ItemType Directory -Force -Path $parent|Out-Null }
    $oldEap=$ErrorActionPreference
    $oldNative=$null
    $hasNativePref=$false
    if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
        $hasNativePref=$true
        $oldNative=$PSNativeCommandUseErrorActionPreference
        $PSNativeCommandUseErrorActionPreference=$false
    }
    try {
        $ErrorActionPreference='Continue'
        & $script:FinalPython @Arguments 2>&1 | Out-File $Path -Encoding utf8
        $code=$LASTEXITCODE
    }
    finally {
        $ErrorActionPreference=$oldEap
        if ($hasNativePref) { $PSNativeCommandUseErrorActionPreference=$oldNative }
    }
    return $code
}

function Assert-PassJson {
    param([string]$Path,[string]$Prefix='PASS_')
    if (!(Test-Path $Path)) { throw "Missing JSON: $Path" }
    $j=Get-Content -Raw $Path|ConvertFrom-Json
    if (-not ([string]$j.decision).StartsWith($Prefix)) { throw "Not PASS: $Path decision=$($j.decision)" }
}
