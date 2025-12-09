# Resolve the current directory path
$parentFolderPath = (Resolve-Path ".").Path

# Define the relative paths to the target folders
$targetFolders = @(
    "ResourceDump\DemandOutputDump",
    "ResourceDump\IncidentDump",
	"ResourceDump\ServiceDeskDump",
    "ResourceDump\SoPDump\SoPData",
    "ResourceDump\SoPDump\SoPFile",
    "Backend\IncidentDumpHandler\TicketAnalysis\output",
    "Backend\IncidentDumpHandler\ESOARAnalysis\output",
    "Backend\FSDDesignHandler\output",
    "Backend\FSDDesignHandler\Temp",
    "Backend\FSDDesignHandler\uploads",
    "SubmittedFiles\IncidentFiles",
    "SubmittedFiles\ServiceDeskFiles",
    "TempFilesDump"
)

# Loop through each target folder and clear its contents
foreach ($relativePath in $targetFolders) {
    $fullPath = Join-Path $parentFolderPath $relativePath
    if (Test-Path $fullPath) {
        try {
            Get-ChildItem -Path $fullPath -Recurse -Force | Remove-Item -Recurse -Force
        } catch {
            Write-Output "ERROR - $($_)"
        }
    }
}