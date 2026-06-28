param(
  [Parameter(Mandatory=$true)][string[]]$Files,
  [int]$W = 1080,
  [int]$H = 1350
)
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (!(Test-Path $edge)) { $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
foreach ($f in $Files) {
  $full = (Resolve-Path $f).Path
  $out  = [System.IO.Path]::ChangeExtension($full, ".png")
  $tmp  = Join-Path $env:TEMP ("edge_" + [guid]::NewGuid().ToString("N"))
  $tpng = Join-Path $env:TEMP ([guid]::NewGuid().ToString("N") + ".png")
  $uri  = "file:///" + (($full -replace '\\','/') -replace ' ','%20')
  $a = @('--headless','--disable-gpu','--no-sandbox','--hide-scrollbars',
         '--force-device-scale-factor=1',"--user-data-dir=$tmp",
         "--window-size=$W,$H",'--virtual-time-budget=4500',
         '--default-background-color=00000000',"--screenshot=$tpng",$uri)
  Start-Process -FilePath $edge -ArgumentList $a -Wait -NoNewWindow | Out-Null
  if (Test-Path $tpng) { Copy-Item $tpng $out -Force; Write-Output ("ok  " + [System.IO.Path]::GetFileName($out)) }
  else { Write-Output ("FAIL " + $f) }
}
