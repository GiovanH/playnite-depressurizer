function DepressurizerExport()
{
    param(
        $scriptMainMenuItemActionArgs
    )
	
	$results = @()
	foreach ($game in $PlayniteApi.MainView.FilteredGames) {
		$details = @{            
			Nane             = $game.name             
			CompletionStatus = $game.CompletionStatus                 
			GameId           = $game.GameId              
			Source           = $game.Source
		}                           
		$results += New-Object PSObject -Property $details  
	}
	
	Write-Host "Writing csv playniteexport.csv"
	$CsvPath="$env:APPDATA\Depressurizer\playniteexport.csv"
	$results | export-csv -Path $CsvPath -NoTypeInformation
	
	Write-Host "Running python conversion"
	py -3 csvToProfile.py $CsvPath
	
    $PlayniteApi.Dialogs.ShowMessage("Saved playnite depressurizer profile.")
}

function GetMainMenuItems()
{
    param(
        $getMainMenuItemsArgs
    )

    $menuItem = New-Object Playnite.SDK.Plugins.ScriptMainMenuItem
    $menuItem.Description = "Export for Depressurizer"
    $menuItem.FunctionName = "DepressurizerExport"
    $menuItem.MenuSection = "@"
	return $menuItem
}