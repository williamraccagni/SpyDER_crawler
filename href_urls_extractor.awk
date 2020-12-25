#BEGIN {RS =" "}
#
#{ for (i=0; i<NF; i++){
#  	if($i~/href/){
#  		sub(/ng-href=(\\)*"/,"",$i)
#  		sub(/href=(\\)*"/,"",$i)
#  		#sub(/href=\\"/,"",$i)
#  		sub(/(\\)*".*/,"",$i)		 # elimino quello che c'è dopo gli url
#  		sub("#","",$i)				 # elimino asterischi
#  		sub(/(\t)+/,"",$i)			 # elimino tab
#  		print $i
#  		}
#	}
#}

BEGIN {RS =" "}

{ for (i=0; i<NF; i++)
  	if($i~/href/){
  	match($i, "\"(http|/).*\"")
    x = substr($i, RSTART, RLENGTH)
    print substr(x, 2, length(x)-2)
}
}
