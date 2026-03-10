# Upload to PyPI using environment variables
# Make sure to set your PyPI token in.env file first

Write-Host "Loading environment variables from .env..." -ForegroundColor Cyan

if (Test-Path ".env") {
   Get-Content .env | ForEach-Object {
        $line = $_.Trim()
        if ($line-match '^([^#=]+)=(.*)$' -and -not $line.StartsWith('#')) {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "User")
            Write-Host "Set $key" -ForegroundColor Green
        }
    }
    Write-Host "`nEnvironment variables loaded!" -ForegroundColor Green
} else {
    Write-Host "Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Please create a .env file with your PyPI API token" -ForegroundColor Yellow
}

Write-Host "`nBuilding package..." -ForegroundColor Cyan
hatch build

Write-Host "`nUploading to PyPI..." -ForegroundColor Cyan

# Extract password from .env file and pass it directly to twine
$envContent = Get-Content .env
$passwordLine = $envContent | Where-Object { $_ -match '^TWINE_PASSWORD=' }
$pypiToken = $passwordLine.Split('=')[1].Trim()

if ($pypiToken) {
    twine upload dist/* --username __token__ --password $pypiToken
} else {
    Write-Host "Error: Could not find TWINE_PASSWORD in .env file" -ForegroundColor Red
    exit 1
}

Write-Host "`nUpload complete!" -ForegroundColor Green
