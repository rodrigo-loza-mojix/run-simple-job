# !/bin/bash
url="https://red.vizix.io/statemachine-api-configuration/rest/configuration/hub"
apikey="CBTP0IEXSMRDRSEE"
filespath="/opt/options/hub_ids/"

while [[ true ]]; do
  # Retrieve hubs.
  hubs=($(curl -X GET -H "apikey: ${apikey}" ${url} | jq -r ".[].id"))
  
  # Create hubs based on retrieved input.
  are_there_files=$(ls ${filespath} | wc -l)
  echo "Are there files in ${filespath} : " ${are_there_files}
  if [[ "${are_there_files}" -gt 0 ]]; then
  	  echo "Removing filenames in ${filespath}"
      rm "${filespath}"/*
  fi;
  are_there_files=$(ls ${filespath} | wc -l)
  echo "Are there files in ${filespath} : " ${are_there_files}
  echo "Updating filenames in ${filespath}"
  for ((index=0; index<"${#hubs[@]}"; index++)); do
      filename="${hubs[${index}]}"
      touch "${filespath}"/"${filename}"
  done;
  are_there_files=$(ls ${filespath} | wc -l)
  echo "Are there files in ${filespath} : " ${are_there_files}

  # Sleep
  sleep 120s
done;

