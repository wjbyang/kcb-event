echo "Deleting database and migration files, rerunning migration..."
scripts/migrate.sh &> /dev/null
echo "...done."
if [ "$2" = "debug" ]; then
    python -m debugpy --listen 127.0.0.1:5678 --wait-for-client manage.py runserver &
    SERVER_PID=$!
    sleep 3
else
    python manage.py runserver &> /dev/null & 
    SERVER_PID=$!
    sleep 0.5
fi

# organization
if [[ -z "$1" || "$1" == "organization" || "$1" == "all" ]]; then
    echo "\nORGANIZATION TEST START"
    source scripts/organization_apis.sh
else 
    source scripts/organization_apis.sh &> /dev/null
fi

# group
if [[ -z "$1" || "$1" == "group" || "$1" == "all" ]]; then
    echo "\nGROUP TEST START"
    source scripts/group_apis.sh "$organization_id"
else 
    source scripts/group_apis.sh "$organization_id" &> /dev/null
fi

# user
if [[ -z "$1" || "$1" == "user" || "$1" == "all" ]]; then
    echo "\n\nUSER TEST START"
    source scripts/user_apis.sh "$organization_id" "$group_id"
else
    source scripts/user_apis.sh "$organization_id" "$group_id" &> /dev/null
fi

# event
if [[ -z "$1" || "$1" == "event" || "$1" == "all" ]]; then
    echo "\n\nEVENT TEST START"
    source scripts/event_apis.sh "$organization_id"
else
    source scripts/event_apis.sh "$organization_id" &> /dev/null
fi

# user to event
if [[ -z "$1" || "$1" == "usertoevent" || "$1" == "all" ]]; then
    echo "\n\nUSER TO EVENT TEST START"
    source scripts/user_to_event_apis.sh "$user_id" "$event_id"
else
    source scripts/user_to_event_apis.sh "$user_id" "$event_id" &> /dev/null
fi

if kill -0 $SERVER_PID > /dev/null 2>&1; then
    echo "\nKilling server process $SERVER_PID."
    kill $SERVER_PID
else
    echo "\nServer process $SERVER_PID not found or already terminated."
fi
lsof -ti:5678 | xargs kill -9