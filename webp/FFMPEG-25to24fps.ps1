Add-Type -AssemblyName System.Windows.Forms
$FolderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$FolderBrowser.Description = 'folder with .webp files'
$FolderBrowser.RootFolder = [System.Environment+specialfolder]::Desktop
$FolderBrowser.ShowNewFolderButton = $true
$DirStatus = $FolderBrowser.ShowDialog()


if ( $DirStatus -eq "OK" ){
    $selectedPath = $FolderBrowser.SelectedPath
    # get all .webp files in the directory
    $videos = Get-ChildItem $selectedPath -Filter *.mov
    foreach ($vid in $videos) {
        $FPS = ffprobe -v 0 -select_streams v -print_format flat -show_entries stream=avg_frame_rate -of default=noprint_wrappers=1:nokey=1 $vid
        if ($FPS -eq "25/1") {
            Write-Host Converting $vid.BaseName
            # output file will be written in the same directory with .mov extension
            $outputName = $vid.DirectoryName + "\" + $vid.BaseName + "_24fps.mov"
            # do ffmpeg conversion
            ffmpeg -y -loglevel quiet -itsscale 1.04166666667 -i $vid.FullName -codec copy $outputName
        }
    }
}
