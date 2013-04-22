'''
Created on 15/04/2013

@author: Oswaldo Neto
'''
import os
import ConfigParser

class Config(ConfigParser.SafeConfigParser):
    def __init__(self, path=None, fp=None, do_load=True):
        ConfigParser.SafeConfigParser.__init__(self)
        path = os.getenv('COLLECT_CONFIG', '/etc/collect.cfg')
        try:
            self.readfp(open(path))
        except:
            raise EnvironmentError("Could not found collect.cfg. Please check COLLECT_CONFIG environment variable or default location /etc/collect.cfg in Linux/Unix.")
        
    def get_db_engine(self, default=None):
        return self.get('database', 'db_engine')
    
    def get_db_name(self, default=None):
        return self.get('database', 'db_name')

    def get_db_host(self, default=None):
        return self.get('database', 'db_host')

    def get_db_port(self, default=None):
        return self.get('database', 'db_port')

    def get_db_user(self, default=None):
        return self.get('database', 'db_user')

    def get_db_password(self, default=None):
        return self.get('database', 'db_passord')
    
    def get_ix_engine(self, default=None):
        return self.get('index', 'ix_engine')

    def get_ix_path(self, default=None):
        return self.get('index', 'ix_path')

    def get_s3_bucket(self, default=None):
        return self.get('s3', 's3_bucket')

    def get_s3_host(self, default=None):
        return self.get('s3', 's3_host')

    def get_s3_bucket_location(self, default=None):
        return self.get('s3', 's3_bucket_location')
     
    def get_aws_access_key_id(self, default=None):
        return self.get('aws', 'aws_access_key_id')

    def get_aws_secret_access_key(self, default=None):
        return self.get('aws', 'aws_secret_access_key')
    
    def get(self, section, name, default=None):
        try:
            val = ConfigParser.SafeConfigParser.get(self, section, name)
        except:
            val = default
        return val
    
    
    

