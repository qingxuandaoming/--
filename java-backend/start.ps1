# Set JAVA_HOME
$env:JAVA_HOME = "C:\Program Files\Java\jdk-23"
$env:PATH = "C:\Program Files\Java\jdk-23\bin;" + $env:PATH

Write-Host "Starting Route Planning Backend Service..."
Write-Host "JAVA_HOME: $env:JAVA_HOME"

# Check Java version
Write-Host "Java Version:"
java -version

# Check Maven version
Write-Host "Maven Version:"
mvn -version

# Clean and compile
Write-Host "Compiling project..."
mvn clean compile

if ($LASTEXITCODE -ne 0) {
    Write-Host "Compilation failed!"
    Read-Host "Press Enter to exit"
    exit 1
}

# Start Spring Boot application
Write-Host "Starting Spring Boot application..."
mvn spring-boot:run

if ($LASTEXITCODE -ne 0) {
    Write-Host "Startup failed!"
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"