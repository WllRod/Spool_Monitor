(New-Object -ComObject 'Shell.Application').Windows() | ForEach-Object { 
  $localPath = $_.Document.Folder.Self.Path 
  $localPath
}
