BEGIN {x=0}

/User-agent: \*/ {x=1}
$0 !~ /User-agent: \*/ && $0 ~ /User-agent: */ {x=0}

$1 ~ /Disallow:/ && x==1 {print $2}