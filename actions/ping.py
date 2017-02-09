from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmPing(NapalmBaseAction):

    def run(self, hostname, host_ip, driver, port, credentials, destination, source, ttl=255, pingtout=2, size=100, count=5):

        try:
            # Look up the driver  and if it's not given from the configuration file
            # Also overides the hostname since we might have a partial host i.e. from
            # syslog such as host1 instead of host1.example.com
            #
            (hostname, host_ip, driver, credentials) = self.find_device_from_config(hostname, host_ip, driver, credentials)

            login = self._get_credentials(credentials)

            if not port:
                optional_args=None
            else:
                optional_args={'port': str(port)}

            with get_network_driver(driver)(
                hostname=str(host_ip),
                username=login['username'],
                password=login['password'],
                optional_args=optional_args
            ) as device:

                route = device.ping(destination, source, ttl, pingtout, size, count)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, route)