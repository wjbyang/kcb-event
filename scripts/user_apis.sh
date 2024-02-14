organization_id=$1
group_id=$2
echo "\n1. Creating a User:"
user_response=$(curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/user \
    -H "Content-Type: application/json" \
    -d "{\
        \"first_name\": \"random-first-name\",\
        \"last_name\": \"random-last-name\",\
        \"email\": \"random@something.com\",\
        \"image\": \"random-image-url\",\
        \"group_id\": \"$group_id\",\
        \"organization_id\": \"$organization_id\"\
    }") &> /dev/null
user_http_status=${response: -3}
user_data=${user_response%???}
echo Status code was $user_http_status.
echo $user_data
user_id=$(echo "$user_data" | jq -r '.data.guid')

echo "\n2. Getting the User that I just created:"
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/user/$user_id

echo "\n\n3. Getting all Users:"
curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/user \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"random-first-name\",
            \"last_name\": \"random-last-name\",
            "email": "\"random1@something.com\"",
            "group_id": "\"$group_id\"",
            "organization_id": "\"$organization_id\""
        }" &> /dev/null
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/users