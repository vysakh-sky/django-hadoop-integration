from hdfs import InsecureClient
# client = InsecureClient('http://192.168.1.40:9870', user='john')

# with open('newtest.txt') as reader, client.write('/user/john/newtt.txt') as writer:
#     writer.write(reader.read())

# with client.read('/user/john/numbers.txt') as reader:
#     r = reader.read()


from django.utils.deconstruct import deconstructible
from django.core.files.storage import Storage
from django.conf import settings
from hdfs.ext.kerberos import KerberosClient




@deconstructible
class HadoopStorage(Storage):
    def __init__(self):
        self.hadoop_host = getattr(settings, 'HADOOP_HOST', 'localhost')
        self.hadoop_port = getattr(settings, 'HADOOP_PORT', 14000)
        self.hadoop_user = getattr(settings, 'HADOOP_USER', 'john')
        self.hadoop_secure = getattr(settings, 'HADOOP_SECURE', 'false')

        if self.hadoop_secure:
            self.client = KerberosClient(f'http://{self.hadoop_host}:{self.hadoop_port}')
        else:
            self.client = InsecureClient(f'http://{self.hadoop_host}:{self.hadoop_port}', user=self.hadoop_user)



    # def _open(self, name, mode='rb'):
    #   pass


    def _save(self, name, content):
        # Save the file to HDFS
        with self.client.write(name, overwrite=True) as writer:
            writer.write(content.read())

        return name
    
    def delete(self, name):
        # Implemented using signals
        # delete the file referenced by name
        # self.client.delete(name)
        pass
    
    def update(self, name, content):
        # Update the file in HDFS
        return self._save(name, content)

    def delete_signal(self, name):
        self.client.delete(name)

    def exists(self, name):
        # return True if file already exists, false if available
        return (name in self.client.list('.'))

    def listdir(self, path):
        # list contents of specified path
        # return 2 tuple of lists ([dirs],[files])
        return ([] ,self.client.list('.'))

    def size(self, name):
        # return total size in bytes
        return self.client.content(name)['spaceConsumed']

    def url(self, name):
        # return url where contents of file can be accessed
        return f'http://{self.hadoop_host}:{self.hadoop_port}/webhdfs/v1/user/{self.hadoop_user}/{name}?op=OPEN' # Need to append authentication query param when rendering on client side, either user.name for simple auth, or delegation token for kerberos
        # return f'http://{self.hadoop_host}:{self.hadoop_port}/webhdfs/v1/user/{self.hadoop_user}/{name}?op=OPEN&user.name={self.hadoop_user}'
    

