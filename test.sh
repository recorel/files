if [ -e /tmp/script.lock ]; then
  echo "script is already running"
  exit 1
else
  /usr/bin/touch /tmp/script.lock
  echo "run script..."
fi

sleep 600
 rm /tmp/script.lock
