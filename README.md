To start:

```
vagrant up
vagrant ssh
```

Then:

```
cd /vagrant/scripts
./install.sh  # installs Elasticsearch and Kibana
cd sentry
./bootstrap.sh
./run.sh  # installs Sentry
```


Add `192.168.100.100 devmeter` to `/etc/hosts` or `C:\Windows\System32\Drivers\etc\hosts`

Access on:

    - http://devmeter - Sentry
    - http://devmeter:9200 - Elasitcsearch
    - http://devmeter:5601 - Kibana
    - http://devmeter:8080 - Jira


In `kibana-tutorial` run the script to prepare data for tutorial then follow the
tutorial.
