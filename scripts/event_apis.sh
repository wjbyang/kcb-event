organization_id=$1
echo "\n1. Creating an Event:"
event_response=$(curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/event \
    -H "Content-Type: application/json" \
    -d "{\
        \"name\": \"random-event-name\",\
        \"location\": \"random-location\",\
        \"description\": \"random-description\",\
        \"image\": \"random-image-url\",\
        \"start_time\": \"2023-01-01T00:00:00Z\",\
        \"organization_id\": \"$organization_id\"
    }") &> /dev/null
event_http_status=${event_response: -3}
event_data=${event_response%???}
echo Status code was $event_http_status.
echo $event_data
event_id=$(echo "$event_data" | jq -r '.data.guid')

echo "\n2. Getting the Event that I just created:"
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/event/$event_id

echo "\n\n3. Getting all Events:"
curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/event \
    -H "Content-Type: application/json" \
    -d "{\
        \"name\": \"another-random-event-name\",\
        \"location\": \"another-random-location\",\
        \"description\": \"another-random-description\",\
        \"start_time\": \"2023-02-02T00:00:00Z\",\
        \"organization_id\": \"$organization_id\"\
    }" &> /dev/null
curl -X GET http://127.0.0.1:8000/eventScheduler/v1/events