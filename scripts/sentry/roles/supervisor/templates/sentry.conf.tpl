[program:sentry-web]
user=ubuntu
directory={{ sentry.virtualenv }}
command={{ sentry.virtualenv }}bin/sentry --config=/etc/sentry/sentry.conf.py run web -l warning
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=syslog
stderr_logfile=syslog

[program:sentry-worker]
user=ubuntu
directory={{ sentry.virtualenv }}
command={{ sentry.virtualenv }}bin/sentry --config=/etc/sentry/sentry.conf.py run worker -l warning
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=syslog
stderr_logfile=syslog

[program:sentry-cron]
user=ubuntu
directory={{ sentry.virtualenv }}
command={{ sentry.virtualenv }}bin/sentry --config=/etc/sentry/sentry.conf.py run cron -l warning
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=syslog
stderr_logfile=syslog
