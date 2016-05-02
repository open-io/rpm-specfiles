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
import json
import os


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
            'path': 'openio',
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
                self.log.error('No configuration found for namespace ' + ns)
                continue
            proxy = config['proxy']
            self.get_stats(http, ns, proxy)

    def get_stats(self, http, namespace, proxy):
        try:
            srvtypes = json.loads(http.request(
                'GET',
                "%s/v3.0/%s/conscience/info?what=types" % (proxy, namespace)
                ).data)
        except Exception as exc:
            self.log.error("Unable to connect to proxy at %s: %s", proxy, exc)
            return
        for srvtype in srvtypes:
            try:
                services = http.request('GET',
                                        "%s/v3.0/%s/conscience/list?type=%s" %
                                        (proxy, namespace, srvtype))
            except Exception as exc:
                self.log.error("Unable to connect to proxy at %s: %s",
                               proxy, exc)
                return
            services = json.loads(services.data)
            # assume that all local services are listening
            # on the same IP address as the proxy
            proxy_ip = proxy.split('//', 1)[-1].split(":", 1)[0] + ":"
            for s in (x for x in services
                      if x.get('addr', "").startswith(proxy_ip)):
                metric_prefix = "%s.%s.%s" % (namespace,
                                              srvtype,
                                              s['addr'].replace('.', '_'))
                metric_value = self.cast_str(s['score'])
                if not isinstance(metric_value, basestring):
                    self.publish(metric_prefix + ".score", metric_value)
                if srvtype == 'rawx':
                    self.get_service_diskspace(
                        metric_prefix, s.get("tags", {}).get('tag.vol', '/'))
                    self.get_rawx_stats(http, s['addr'], namespace)
                elif srvtype == 'meta2':
                    self.get_gridd_stats(http, proxy, s['addr'],
                                         namespace, srvtype)

    def get_service_diskspace(self, metric_prefix, volume):
        if hasattr(os, 'statvfs'):  # POSIX
            try:
                data = os.statvfs(volume)
            except OSError, e:
                self.log.exception(e)
                return

            block_size = data.f_bsize
            blocks_total = data.f_blocks
            blocks_free = data.f_bfree
            blocks_avail = data.f_bavail
            inodes_total = data.f_files
            inodes_free = data.f_ffree
            inodes_avail = data.f_favail
        else:
            raise NotImplementedError("platform not supported")

        for unit in self.config['byte_unit']:
            metric_name = '%s.%s_percentfree' % (metric_prefix, unit)
            metric_value = float(blocks_free) / float(
              blocks_free + (blocks_total - blocks_free)) * 100
            self.publish_gauge(metric_name, metric_value, 2)

            metric_name = '%s.%s_used' % (metric_prefix, unit)
            metric_value = float(block_size) * float(
                blocks_total - blocks_free)
            metric_value = diamond.convertor.binary.convert(
              value=metric_value, oldUnit='byte', newUnit=unit)
            self.publish_gauge(metric_name, metric_value, 2)

            metric_name = '%s.%s_free' % (metric_prefix, unit)
            metric_value = float(block_size) * float(blocks_free)
            metric_value = diamond.convertor.binary.convert(
              value=metric_value, oldUnit='byte', newUnit=unit)
            self.publish_gauge(metric_name, metric_value, 2)

            metric_name = '%s.%s_avail' % (metric_prefix, unit)
            metric_value = float(block_size) * float(blocks_avail)
            metric_value = diamond.convertor.binary.convert(
              value=metric_value, oldUnit='byte', newUnit=unit)
            self.publish_gauge(metric_name, metric_value, 2)

        if float(inodes_total) > 0:
            self.publish_gauge(
              '%s.inodes_percentfree' % metric_prefix,
              float(inodes_free) / float(inodes_total) * 100)
        self.publish_gauge('%s.inodes_used' % metric_prefix,
                           inodes_total - inodes_free)
        self.publish_gauge('%s.inodes_free' % metric_prefix, inodes_free)
        self.publish_gauge('%s.inodes_avail' % metric_prefix, inodes_avail)

    def get_rawx_stats(self, http, addr, namespace, srv_type='rawx'):
        stat = http.request('GET', addr+'/stat')
        for m in (stat.data).split('\n'):
            if not m:
                continue
            metric_type, metric_name, metric_value = m.split(' ')
            metric_value = self.cast_str(metric_value)
            if not isinstance(metric_value, basestring):
                metric_name = "%s.%s.%s.%s" % (namespace,
                                               srv_type,
                                               addr.replace('.', '_'),
                                               metric_name)
                self.publish(metric_name, metric_value,
                             metric_type=metric_type.upper())

    def get_gridd_stats(self, http, proxy, addr, namespace, srv_type):
        stat = http.request('POST', proxy+'/v3.0/forward/stats?id='+addr)
        for m in (stat.data).split('\n'):
            if not m:
                continue
            metric_type, metric_name, metric_value = m.split(' ')
            metric_value = self.cast_str(metric_value)
            if not isinstance(metric_value, basestring):
                metric_name = "%s.%s.%s.%s" % (namespace,
                                               srv_type,
                                               addr.replace('.', '_'),
                                               metric_name)
                self.publish(metric_name, metric_value,
                             metric_type=metric_type.upper())

    def cast_str(self, value):
        """Return string casted to int or float if possible"""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value
