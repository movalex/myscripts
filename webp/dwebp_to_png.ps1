Add-Type -AssemblyName System.Windows.Forms
$FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{
    SelectedPath = "D:\PROJECTS\"
}
[void]$FolderBrowser.ShowDialog()
$FolderBrowser.Description = 'folder with .webp files'
$FolderBrowser.RootFolder = [System.Environment+specialfolder]::Desktop
$FolderBrowser.ShowNewFolderButton = $true
$DirStatus = $FolderBrowser.ShowDialog()

if ( $DirStatus -eq "OK" ){
    $selectedPath = $FolderBrowser.SelectedPath
    # get all .webp files in the directory
    $images = Get-ChildItem $selectedPath -Filter *.webp
    foreach ($img in $images) {
        # output file will be written in the same directory with .png extension
        $outputName = $img.DirectoryName + "\" + $img.BaseName + ".png"
        # copy-paste the path to dwebp program and set its input and output parameters
        # more options https://developers.google.com/speed/webp/docs/dwebp
        dwebp $img.FullName -o $outputName
    }
}
