# !/bin/bash
url="https://red.vizix.io/statemachine-api-configuration/rest/configuration/locations/?level=premise&size=500"
apikey="CBTP0IEXSMRDRSEE"
filespath="/opt/options/premise_codes/"

while [[ true ]]; do
  # Retrieve codes and names.
  codes=($(curl -X GET -H "apikey: ${apikey}" ${url} | jq -r ".[].code"))
  names=($(curl -X GET -H "apikey: ${apikey}" ${url} | jq -r ".[].name" | tr " " "_"))
  
  # Create codes and names based on retrieved input.
  are_there_files=$(ls ${filespath} | wc -l)
  echo "Are there files in ${filespath} : " ${are_there_files}
  if [[ "${are_there_files}" -gt 0 ]]; then
  	  echo "Removing filenames in ${filespath}"
      rm "${filespath}"/*
  fi;
  are_there_files=$(ls ${filespath} | wc -l)
  echo "Are there files in ${filespath} : " ${are_there_files}
  echo "Updating filenames in ${filespath}"
  for ((index=0; index<"${#codes[@]}"; index++)); do
      filename="${names[${index}]}___${codes[${index}]}"
      touch "${filespath}"/"${filename}"
  done;
  are_there_files=$(ls ${filespath} | wc -l)
  echo "Are there files in ${filespath} : " ${are_there_files}

  # Sleep
  sleep 120s
done;

