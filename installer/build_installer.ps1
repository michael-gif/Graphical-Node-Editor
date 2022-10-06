$arr = Get-ChildItem "C:\Program Files (x86)" | 
       Where-Object {$_.PSIsContainer} | 
       Foreach-Object {$_.Name}

$installationDirectory = $null
ForEach ($i in $arr) {
	if ($i.Contains("Inno Setup")) {
        $installationDirectory = "C:\Program Files (x86)\" + $i
        break
    }
}

Write-Host $installationDirectory
if ($installationDirectory -ne $null) {
	& "$installationDirectory\iscc.exe" ".\installer\installer_script.iss"
}