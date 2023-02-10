#!/bin/bash
# bash script to generate yaml files from template and properties file
# usage: ./parse_yaml.sh <template.yaml> <properties.yaml>
# example: ./parse_yaml.sh spawn-tasks-template.yaml spawn-tasks-values.yaml

# function that takes a line and returns the key and value
function parse_line() {
    line=$1
    key=$(echo "$line" | cut -d ':' -f1 | xargs)

    if [[ $key == -* ]]; then
        key=$(echo "$key" | sed 's/^- //')
    fi

    value=$(echo "$line" | cut -d ':' -f2 | xargs)
    echo "$key:$value"
}



if [ $# -ne 2 ]; then
    echo "Usage: $0 <template.yaml> <properties file>"
    exit 1
fi

template=$1
properties=$2
output=""

if [ ! -f $template ]; then
    echo "Template file $template does not exist"
    exit 1
fi

if [ ! -f $properties ]; then
    echo "Properties file $properties does not exist"
    exit 1
fi


while read line; do
  key_value=$(parse_line "$line")
  key=$(echo "$key_value" | cut -d ':' -f1)
  value=$(echo "$key_value" | cut -d ':' -f2)
  if [[ $key == "fileName" ]]; then
      output="${value}.yaml"
      cp $template $output
      echo "writing yaml file for $output"
  elif [[ $output != "" ]]; then
      sed -i "s|{{ ${key} }}|\"${value}\"|g" $output
  fi
done < $properties


exit 0









