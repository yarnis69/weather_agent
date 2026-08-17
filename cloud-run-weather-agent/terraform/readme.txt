The following is required before the initial terraform apply

- increment the github_actions_pool name (due to previous deletion being soft)


The following manual tasks after first terraform apply is made

- manually push agent docker image:

docker build -t europe-west2-docker.pkg.dev/weather-agent-504614/weather-agent-repo/weather-agent:v1 .
docker run -p 8080:8080 europe-west2-docker.pkg.dev/weather-agent-504614/weather-agent-repo/weather-agent
docker push europe-west2-docker.pkg.dev/weather-agent-504614/weather-agent-repo/weather-agent:v1

- manually give Gemini-API-Key Secret a value (excluded for security reasons)

