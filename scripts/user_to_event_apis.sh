user_id=$1
event_id=$2

eventattendingresponse=$(curl -s -w "%{http_code}" -X POST http://127.0.0.1:8000/eventScheduler/v1/eventattending \
    -H "Content-Type: application/json" \
    -d "{\
        \"user_id\": \"$user_id\",\
        \"event_id\": \"$event_id\",\
        \"attending\": \"True\"
    }") &> /dev/null

eventattending_http_status=${eventattendingresponse: -3}
eventattendingdata=${eventattendingresponse%???}
echo Status code was $eventattending_http_status.
echo $eventattendingdata