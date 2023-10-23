# Prompt user for source and destination paths
$source = Read-Host "Enter the source path of the files to link (leave blank for current directory)"

if ($source -eq "") {
    $source = Get-Location
}

$destination = Read-Host "Enter the destination path for the links"

# Get selected files
$files = Get-ChildItem -Path $source -File -Filter "*.jsx"

# Create symbolic links for each file
foreach ($file in $files) {
    $linkPath = Join-Path $destination $file.Name
    New-Item -ItemType SymbolicLink -Path $linkPath -Target $file.FullName -Force
}
