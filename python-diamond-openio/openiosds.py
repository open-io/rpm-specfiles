# coding=utf-8

"""
Collect OpenIO SDS stats



#### Dependencies

 * urllib3
 * oiopy
 * ast
 * json

#### Example Configuration

OpenIOSDSCollector.conf

```
    enabled = True
    namespaces = NS1, NS2, ...
```

"""


import diamond.collector
import urllib3
import oiopy.utils
import ast
import json
import string
import re


class OpenIOSDSCollector(diamond.collector.Collector):


    def get_default_config_help(self):
        config_help = super(OpenIOSDSCollector, self).get_default_config_help()
        config_help.update({
            'namespaces': "List of namespaces (comma separated)",
        })
        return config_help


    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(OpenIOSDSCollector, self).get_default_config()
        config.update({
            'path':     'openio',
            # Namespaces
            'namespaces': ['OPENIO'],
        })
        return config


    def collect(self):
        namespaces = self.config.get('namespaces')

        # Convert a string config value to be an array
        if isinstance(namespaces, basestring):
            namespaces = [namespaces]

        http = urllib3.PoolManager()

        for ns in namespaces:
            config = oiopy.utils.load_sds_conf(ns)
            if not config:
              self.log.error('No configuration not found for namespace '+ns)
              continue
            proxy = config['proxy']
            self.get_stats(http,ns,proxy)


    def get_stats(self, http, namespace, proxy):

        service_types = http.request('GET', proxy+'/v3.0/'+namespace+'/conscience/info?what=types')
        service_types = ast.literal_eval(service_types.data)
        for srv_type in service_types:
            services = http.request('GET', proxy+'/v3.0/'+namespace+'/conscience/list?type='+srv_type)
            services = json.loads(services.data)
            for s in services:
                 metric_name = srv_type+'.'+string.replace(s['addr'],'.','_')+'.score'
                 metric_value = self.cast_str(s['score'])
                 if not isinstance(metric_value, basestring):
                     self.publish(metric_name, metric_value)
                 if srv_type == 'rawx':
                     self.get_rawx_stats(http,s['addr'])
                 elif srv_type == 'meta2':
                     self.get_gridd_stats(http,proxy,s['addr'],srv_type)


    def get_rawx_stats(self,http,addr,srv_type='rawx'):
        stat = http.request('GET', addr+'/stat')
        for m in (stat.data).split('\n'):
            if not m:
                continue
            metric_type, metric_name, metric_value = m.split(' ')
            metric_value = self.cast_str(metric_value)
            if not isinstance(metric_value, basestring):
                metric_name = srv_type+'.'+string.replace(addr,'.','_')+'.'+metric_name
                self.publish(metric_name, metric_value,metric_type=metric_type.upper())


    def get_gridd_stats(self,http,proxy,addr,srv_type):
        stat = http.request('POST', proxy+'/v3.0/forward/stats?id='+addr)
        for m in (stat.data).split('\n'):
            if not m:
                continue
            metric_type, metric_name, metric_value = m.split(' ')
            metric_value = self.cast_str(metric_value)
            if not isinstance(metric_value, basestring):
                metric_name = srv_type+'.'+string.replace(addr,'.','_')+'.'+metric_name
                self.publish(metric_name, metric_value,metric_type=metric_type.upper())


    # Return string casted to int or float if possible
    def cast_str(self,value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

