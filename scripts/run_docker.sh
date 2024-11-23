IMAGE_NAME="project-ml"
CONTAINER_NAME="project-ml"

docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true
docker build -t "$IMAGE_NAME" . && docker run --name "$CONTAINER_NAME" -p 8080:8080 "$IMAGE_NAME"
