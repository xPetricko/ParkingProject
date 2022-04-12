if ! command -v nvidia-smi &> /dev/null
then
    echo "nvidia-smi could not be found"
    echo "Starting no GPU docker app"
    docker compose -f docker-compose-no-gpu.yml up -d
else
    echo "Starting docker app with GPU capability"
    docker compose -f docker-compose-gpu.yml up -d
fi