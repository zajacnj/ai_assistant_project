# VA AI Assistant - Auto Port Finder (PowerShell)
# This script finds an available port and starts the Streamlit app

$basePort = 8502
$maxPort = 8510
$foundPort = $null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VA AI Assistant - Auto Port Finder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if port is available
function Test-PortAvailable {
    param([int]$Port)
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    }
    catch {
        return $false
    }
}

# Find available port
for ($port = $basePort; $port -le $maxPort; $port++) {
    if (Test-PortAvailable -Port $port) {
        $foundPort = $port
        Write-Host "✓ Found available port: $port" -ForegroundColor Green
        break
    }
    else {
        Write-Host "⨯ Port $port is in use, trying next..." -ForegroundColor Yellow
    }
}

if ($null -eq $foundPort) {
    Write-Host ""
    Write-Host "ERROR: No available ports found between $basePort and $maxPort" -ForegroundColor Red
    Write-Host "Please close some applications or manually specify a different port." -ForegroundColor Red
    Read-Host -Prompt "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting app on port $foundPort..." -ForegroundColor Green
Write-Host "App will open at http://localhost:$foundPort" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start Streamlit
& py -3 -m streamlit run "main.py" --server.port=$foundPort --server.fileWatcherType=poll --server.runOnSave=true
