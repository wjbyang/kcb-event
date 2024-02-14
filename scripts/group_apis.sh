organization_id=$1

echo "\n1. Creating a Group:"
group_response=$(curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/group \
    -H 'Content-Type: application/json' \
    -d '{"name": "random-group", "organization_id": "$organization_id"}')
group_http_status=${group_response: -3}
echo Status code was $group_http_status.
group_id=$(echo "${group_response%???}" | jq -r '.guid')

echo "\n2. Getting the Group that I just created:"
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/group/$group_id

echo "\n\n3. Getting all Groups:"
curl -X POST http://127.0.0.1:8000/eventScheduler/v1/group \
    -H 'Content-Type: application/json' \
    -d '{
            "name": "another-group-that-was-just-added",
            "organization_id": "$organization_id"
        }' &> /dev/null
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/groups