
# Bring up dev environment #

# Run this script to bring up the docker container and open shell
# Image must be built before running this script



if [ -n "$(docker compose ps --status running -q dev)" ]; then
    echo "Opening Interactive docker terminal.."
    docker compose exec dev bash
else
    echo "Starting a new container.."
    docker compose up -d
    docker compose exec dev bash
fi