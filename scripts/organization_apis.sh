echo "\n1. Creating an Organization:"
organization_response=$(curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/organization \
    -H 'Content-Type: application/json' \
    -d '{"name": "random-organization"}')
organization_http_status=${organization_response: -3}
echo Status code was $organization_http_status.
organization_id=$(echo "${organization_response%???}" | jq -r '.guid')

echo "\n2. Getting the Organization that I just created:"
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/organization/$organization_id

echo "\n\n3. Getting all Organizations:"
curl -X POST http://127.0.0.1:8000/eventScheduler/v1/organization \
    -H 'Content-Type: application/json' \
    -d '{
            "name": "another-organization-that-was-just-added"
        }' &> /dev/null
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/organizations