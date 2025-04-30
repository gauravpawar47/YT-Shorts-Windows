[Setup]
AppName=YT Shorts Downloader
AppVersion=1.0
DefaultDirName={pf}\YTShortsDownloader
DefaultGroupName=YTShortsDownloader
OutputDir=dist\installer
OutputBaseFilename=YouTubeShortsDownloader_Installer
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "Project\dist\YouTubeShortsDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Project\dist\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YouTube Shorts Downloader"; Filename: "{app}\YouTubeShortsDownloader.exe"

[Run]
Filename: "{app}\YouTubeShortsDownloader.exe"; Description: "Launch YouTube Shorts Downloader"; Flags: nowait postinstall
