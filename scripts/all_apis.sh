echo "Deleting database and migration files, rerunning migration..."
scripts/migrate.sh &> /dev/null
echo "...done."
python manage.py runserver &> /dev/null & 
SERVER_PID=$!
sleep 0.5

# organization
echo "\nORGANIZATION TEST START"
source scripts/organization_apis.sh

# group
echo "\n\nGROUP TEST START"
source scripts/group_apis.sh "$organization_id"

# user
echo "\n\nUSER TEST START"
source scripts/user_apis.sh "$organization_id" "$group_id"

kill $SERVER_PID