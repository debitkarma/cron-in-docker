# Cron in Docker

This is a toy repo to mess around with the union of cron and docker.

## Goals

1. Test running cron jobs inside a docker container.

1. Test running jobs inside a docker container via system cron.

1. Assess which is most viable for a different project I'm working on.

## Takeaways

Generally, the sense is that it's bad form to use cron inside a docker container. Why?

1. Containers should only have one running process.
1. If a second process fails, it may not alert or br captured by logs.
1. Adding infra to a container when a perfectly working one (system) exists adds bulk.
1. No consistency is *gained* by doing this, and some argue that it *may* be lost.
1. System cron can verify permissions, log failures, and notify correctly without additional issues.
1. relevant crontabs can still be version-controlled

Things to watch for:
- Check what perms the container with the script is running under.
- Add the crontab for the relevant user.
- You may need to configure the user's cron/services to run even if they are not logged in.
- The relevant command is something like `docker exec -it COMMAND`

## Resources

- [Sample of running cron inside a docker container, built with example dockerfile (found via a reddit thread)](https://pad.schlosser-ma.de/s/tMcArQWrM#)
- [aforementioned reddit thread](https://www.reddit.com/r/docker/comments/16zobfm/a_good_crontab_docker_container/)
- [Rolling your own cron-enabled container](https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container)