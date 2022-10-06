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
write-host $args[0]
if ($installationDirectory -ne $null) {
    $installationScript = $args[0]
    & "$installationDirectory\iscc.exe" $installationScript
}