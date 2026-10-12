# 설치된 PowerPoint 로 pptx 를 열어 슬라이드마다 PNG 로 내보낸다 (preview/ 폴더).
# 사용법: powershell -ExecutionPolicy Bypass -File scripts\preview.ps1
$root = Split-Path -Parent $PSScriptRoot
$pptx = Get-ChildItem (Join-Path $root "output") -Filter *.pptx | Select-Object -First 1
$out = Join-Path $root "preview"
New-Item -ItemType Directory -Force $out | Out-Null
Get-ChildItem $out -Filter *.png | Remove-Item -Force
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($pptx.FullName, $true, $false, $false)
    foreach ($s in $pres.Slides) {
        $s.Export((Join-Path $out ("slide-{0:D2}.png" -f $s.SlideIndex)), "PNG", 1600, 900)
    }
    $pres.Close()
} finally {
    $app.Quit()
}
Write-Output "exported to $out"
