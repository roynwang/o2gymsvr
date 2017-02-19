sub urlencode {
    my $s = shift;
    $s =~ s/ /+/g;
    $s =~ s/([^A-Za-z0-9\+-])/sprintf("%%%02X", ord($1))/seg;
    return $s;
}

$area = shift;
$query = $area;
if($area eq "北京"){
	$area = 2;
}
if($area eq "厦门"){
	$area = 15;
}
$keyword = "";
while(@ARGV){
	$k = shift;
	if(length($keyword) != 0){
		$keyword.=" ";
	}
	$keyword.= $k;
	$query.=$k;

}
$keyword = urlencode($keyword);
$url = "http://www.dianping.com/search/keyword/$area/0_$keyword";
#print $url."\n";

#while (<>) { $document .= $_ }
$document = `curl http://www.dianping.com/search/keyword/$area/0_$keyword`;
@m = $document =~ /<span class="num">（(\d+)）</g;
$result =  $m[0];

my $current_date = `date +"%Y-%m-%d"`;
$current_date = substr($current_date,0,-1);
$host = "http://o2-fit.com";
$cmd = "curl -d \"keyword=$query&count=$result&date=$current_date\" $host/api/cwl/shopcount/$query/";
print $cmd;
`$cmd`;
