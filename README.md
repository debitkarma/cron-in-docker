# Cron in Docker

This is a toy repo to mess around with the union of cron and docker.


## Goals

1. Test running cron jobs inside a docker container.

1. Test running jobs inside a docker container via system cron.

1. Assess which is most viable for a different project I'm working on.


## Docker commands

You can build this with:

`docker build . -t debitkarma/cron-in-docker:latest`

Then, you just have to have a working `docker-compose.yaml` (use the .yaml extension, not my .yml one), and a filled-in `.env` file in a particular folder. Make sure the image name is in the file exactly as you had it in the build command.

`docker compose up` will run a container with that image, and display the logs in the terminal until it exits.

`docker compose logs` will let you view logs, even after the container has exited and is down.

Use the `dummy-app.service` and `dummy-app.timer` files to get things running on schedule, then you can use the `journalctl` command as you like. You can also use the mapped volume `./log` and view the `history.log` file.

If you run this as a user, be sure to turn on lingering for your user, so that the timers/services work even if you are not logged in. (Check the section at the bottom of this README for that.)

And, if you really want to use cron, check `crontab` to see how to do it via system crontab, or via your user crontab.


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

**TO DO: check to see if user cron works like user systemd service/timer units**

My instinct is just go with systemd services+timers because of the nice journalctl logging that's built in and present, as well as notifications. I may use ntfy or a curl to uptime-kuma for the latter.

- [Reddit thread on systemd vs cron](https://www.reddit.com/r/linuxadmin/comments/k8l272/systemdtimers_vs_cron/) ; this points out the infrastructure that systemd provides, as I stated above.
- [Basic guide on how to create crontab entries and systemd units](https://akashrajpurohit.com/blog/systemd-timers-vs-cron-jobs/)
- [Op-ed piece on why systemd might be preferable for additional reasons](https://anteru.net/blog/2024/replacing-cron-with-systemd-timers/)


###### SystemD units as users require the following changes due to caveats:

> User units may not function correctly after reboot - until that user logs in. In order to enable user units to work on reboot without them having to log in first, or be logged in… Enable “lingering” via
>
> `loginctl enable-linger $USER`

> To look up logs for user units, without sudo and as the user, run:
>
> `journalctl --user-unit $SERVICE_NAME`
>
> If you don't see any logs, it could be (depending on distro) that your journalctl isn't configured for persistence. You can make sure that's enabled via changing `Storage=auto` to `Storage=persistent` in the `/etc/systemd/journald.conf` file. THen restart journald:
>
> sudo systemctl restart systemd-journald.service


## Resources

- [Sample of running cron inside a docker container, built with example dockerfile (found via a reddit thread)](https://pad.schlosser-ma.de/s/tMcArQWrM#)
- [aforementioned reddit thread](https://www.reddit.com/r/docker/comments/16zobfm/a_good_crontab_docker_container/)
- [Rolling your own cron-enabled container](https://stackoverflow.com/questions/37458287/how-to-run-a-cron-job-inside-a-docker-container)
- [Using uv with docker](https://github.com/astral-sh/uv-docker-example)
- [Official integration guide for uv+docker](https://docs.astral.sh/uv/guides/integration/docker/)
- [logging to syslog for systemd services, simultaneously with separate files](https://stackoverflow.com/questions/37585758/how-to-redirect-output-of-systemd-service-to-a-file)

