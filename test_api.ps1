# Test Python Backend API

# Test health check
Write-Host "Testing health check API..."
$healthResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method GET
Write-Host "Health check response: $($healthResponse.Content)"

# Test equipment categories
Write-Host "`nTesting equipment categories API..."
$categoriesResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/equipment/categories" -Method GET
Write-Host "Categories response: $($categoriesResponse.Content)"

# Test equipment search
Write-Host "`nTesting equipment search API..."
$searchUrl = "http://localhost:5000/api/equipment/search?keyword=bike&page=1&per_page=3"
try {
    $searchResponse = Invoke-WebRequest -Uri $searchUrl -Method GET
    Write-Host "Search response: $($searchResponse.Content)"
} catch {
    Write-Host "Search API error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Error response body: $responseBody"
    }
}

Write-Host "`nAll API tests completed!"