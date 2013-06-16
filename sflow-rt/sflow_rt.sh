#!/bin/bash
if [ $1 = 'la' ]
then
        curl "http://localhost:8008/agents/json"
elif [ $1 = 'rm' ]
then
        curl "http://localhost:8008/metric/{mininet}/json"
elif [ $1 = 'dm' ]
then
        curl "http://localhost:8008/dump/{mininet}/{ifoutucastpkts}/json"
elif [ $1 = 'df' ]
then
	#curl -H -X "{keys:'ipsource,ipdestination', value:'frames', filter:'10.0.0.2&10.0.0.1'}" http://localhost:8008/flow/incoming/json
	curl -H "Content-Type:application/json" -X PUT --data "{keys:'ipsource,ipdestination', value:'bytes'}" http://localhost:8008/flow/incoming/json
elif [ $1 = 'gm' ]
then
        curl "http://localhost:8008/metric/{mininet}/incoming/json"
        #curl "http://localhost:8008/flow/{incoming}/json"
else
        echo "Argument did not match !"
fi

