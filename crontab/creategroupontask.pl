$area = shift;
$host = "o2-fit.com";
if($area eq "北京"){
	$area = 'beijing';
}
if($area eq "厦门"){
	$area = 'xiamen';
}

$keyword = "";
while(@ARGV){
	$k = shift;
	if(length($keyword) != 0){
		$keyword.="%20";
	}
	$keyword.= $k;
}
my $current_date = `date +"%Y-%m-%d"`;
chomp($current_date);
my $data = "date=".$current_date."&city=".$area."&keyword=".$keyword;
print $data;
$cmd ="curl -d \"$data\" http://$host/api/cwl/task/ > groupontask";
`$cmd`;
