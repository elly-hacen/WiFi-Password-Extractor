

$listProfiles = netsh wlan show profiles | Select-String -Pattern "All User Profile" | ForEach-Object{ ($_ -split ":")[-1].Trim() };
$listProfiles | ForEach-Object {
	$profileInfo = netsh wlan show profiles name=$_ key="clear";
	$SSID = $profileInfo | Select-String -Pattern "SSID Name" | ForEach-Object{ ($_ -split ":")[-1].Trim() };
	$Key = $profileInfo | Select-String -Pattern "Key Content" | ForEach-Object{ ($_ -split ":")[-1].Trim() };
	[PSCustomObject]@{
		WifiProfileName = $SSID;
		Password = $Key
	}
}
