# Hadoop Filestorage for Django

Django application that implements file storage on a Apache Hadoop cluster.

## Instructions

1. Install requirements.txt in your environment
2. Run migrations ```python manage.py migrate```
3. Setup Hadoop Configuration in settings.py
   ```settings.py
   HADOOP_USER = 'your_hadoop_user'
   HADOOP_HOST = 'your_hadoop_host'
   HADOOP_PORT = 'your_hadoop_port'
   ```

5. Create superuser ```python manage.py createsuperuser```
6. You can add and delete articles from the admin interface at localhost:8000/admin
7. Visit /articles to view all articles


## Hadoop Cluster Setup

For testing purposes, you can set up a single node Hadoop pseudo-cluster. Follow the instructions provided [here](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html).

Instructions to setup a Fully Distributed Cluster can be found [here](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/ClusterSetup.html).

## Notes

- ~~**Insecure WebHDFS**: The current implementation uses insecure [WebHDFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/WebHDFS.html) or [HttpFS](https://hadoop.apache.org/docs/current/hadoop-hdfs-httpfs/) API.~~ Secure access has been implemented through Kerberos Authentication - [Secure Hadoop Cluster Setup](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SecureMode.html)