To convert .webp files to a .png on Windows:

* download the latest version of libwebp from Google: https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.2.0-rc3-windows-x64.zip
* unarchive the folder to your user folder
* add the environment variable pointing to the `bin` folder in unarchived directory to your local Windows $Path (see the screenshot)
* in the Console run command `dwebp <filename.webp> -o <output_filename.png>`

Or use this powershell script.
The script will launch an open folder dialog and will process all `.webp` files in the folder you've selected creating `.png` files in that folder. Right click the `ps1` file and choose `Run with Powershell` 
