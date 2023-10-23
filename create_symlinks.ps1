# Prompt user for source and destination paths
$source = Read-Host "Enter the source path of the files to link (leave blank for current directory)"

if ($source -eq "") {
    $source = Get-Location
}

$destination = Read-Host "Enter the destination path for the links"
if ($destination -eq "") {
    $destination = "C:\Program Files\Adobe\Adobe Photoshop 2023\Presets\Scripts"
}

# Get all jsx files in all folders
# $files = Get-ChildItem -Path $source -File -Filter "*.jsx" -Recurse

# Get all current files and directories
$items = Get-ChildItem -Path $source


Function CreateSymlinks($link, $target) {
    $ext = [IO.Path]::GetExtension($target)
    if ($ext -like ".js*") {
        New-Item -ItemType SymbolicLink -Path $link -Target $target.FullName -Force
    }
    else {
        Write-Host("Skipping file {0}" -f $link)
    }
}


Function CreateFolders($folderPath) {
    if (-not (Test-Path $folderPath)) {
        New-Item -ItemType Directory -Path $folderPath
        Write-Host("Folder {0} created" -f $item.Name )
    }
    else {
        Write-Host("Folder already exists")
    }
}

# Create symbolic links for each file and directory
function Main($items, $destination) {
    foreach ($item in $items) {
        # Check if item is a directory
        if (Test-Path $item.FullName -PathType Container) {
            Write-Host "$($item.Name) is a directory"
            # Create destination folder if it doesn't exist
            $folderPath = Join-Path $destination $item.Name
            CreateFolders $folderPath

            # run the function recursvely for all the files in the folder
            $targetfolder = Join-Path $source $item.Name 
            $folderItems = Get-ChildItem -Path $targetfolder

            Main $folderItems $folderPath
        }
        else {
            $linkPath = Join-Path $destination $item.Name
            Write-Host("Linking file: {0}" -f $linkPath)
            CreateSymlinks -link $linkPath -target $item
        }
    }
}
Main $items $destination