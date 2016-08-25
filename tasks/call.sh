#!/bin/bash

URL=$1
ID=$2
TEXT=$3

curl -XPOST -H "Content-Type: application/json" \
	$URL \
	-d "{\"message\": \
			{	\"text\": \"$TEXT\", \
				\"from\": {\
					\"id\": \"$ID\",\
					\"first_name\": \"test_first_name\",\
					\"second_name\": \"test_second_name\",\
					\"username\": \"test_username\"\
				}\
			}\
		}"