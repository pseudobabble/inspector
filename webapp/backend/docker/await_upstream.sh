#!/bin/sh
echo "Attempting to connect to GraphQL server @ dagster-dagit:3000"
until $(nc -zv dagster-dagit 3000); do
  echo "Retrying"
  sleep 5
done

echo "Connected"
exec "${@}"
