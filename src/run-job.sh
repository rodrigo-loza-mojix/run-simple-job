#!/bin/bash
log_level=${LOG_LEVEL:=INFO}
streamapps=(rulesprocessor mongoinjector actionprocessor transformbridge hbridge reportgenerator m2k k2m)

for streamapp in ${streamapps[@]}; do
  echo "Updating ${streamapp} log level to ${log_level}"
	for ((i=0; i<10; i++)); do
		curl -H 'Content-type: text/plain' http://"${streamapp}":8000/config/log -X POST -d "com.tierconnect=${log_level}"
		if [[ $? -ne 0 ]]; then
			echo "Streamapp ${streamapp} failed to update its log level to ${log_level}"
		fi;
	done;
  echo ""
done;

