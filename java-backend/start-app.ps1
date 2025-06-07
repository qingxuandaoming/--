# Set Java environment
$env:JAVA_HOME = 'C:\PROGRA~1\Java\jdk-23'
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# Display Java version
Write-Host "Java Home: $env:JAVA_HOME"
java -version

# Clean and compile first
Write-Host "Cleaning and compiling project..."
mvn clean compile

if ($LASTEXITCODE -eq 0) {
    # Start Spring Boot application
    Write-Host "Starting Spring Boot application..."
    mvn spring-boot:run
} else {
    Write-Host "Compilation failed. Please check the errors above."
}