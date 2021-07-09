
docker system df                 # количество используемых ресурсов докером



# =============================================================================================================================
# DOCKER HUB
# =============================================================================================================================

docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"

docker build -f Dockerfile -t $DOCKER_USER_ID/sentiment-analysis-frontend .

docker push $DOCKER_USER_ID/sentiment-analysis-frontend




