# coding=utf-8

"""
The SimpleCollector collects one utilization metric for CPU, MEM, Disk I/O, and Disk Usage

"""

import diamond.collector
import os

class SimpleCollector(diamond.collector.Collector):

    PROC = '/proc/stat'

    def __init__(self, config=None, handlers=[], name=None, configfile=None):
        super(SimpleCollector, self).__init__(config, handlers, name, configfile)


    def get_default_config_help(self):
        return super(SimpleCollector, self).get_default_config_help()

    def get_default_config(self):
        config = super(SimpleCollector, self).get_default_config()
        config.update({
            'path': 'netuitive.linux',
        })
        return config

    def collect(self):
        if os.access(self.PROC, os.R_OK):
            file = open(self.PROC)
            lines = file.read().splitlines()
            file.close()

            for line in lines:
                if line.startswith('cpu '):
                    elements = line.split()
                    self.collect_cpu_proc(elements)

        return True

    def collect_cpu_proc(self, elements):
        # Compute all CPU usage values from /proc/stat counter values
        user = self.derivative('cpu.total.user', long(elements[1]), diamond.collector.MAX_COUNTER)
        nice = self.derivative('cpu.total.nice', long(elements[2]), diamond.collector.MAX_COUNTER)
        system = self.derivative('cpu.total.system', long(elements[3]), diamond.collector.MAX_COUNTER)
        idle = self.derivative('cpu.total.idle', long(elements[4]), diamond.collector.MAX_COUNTER)
        iowait = self.derivative('cpu.total.iowait', long(elements[5]), diamond.collector.MAX_COUNTER)
        irq = self.derivative('cpu.total.irq', long(elements[6]), diamond.collector.MAX_COUNTER)
        softirq = self.derivative('cpu.total.softirq', long(elements[7]), diamond.collector.MAX_COUNTER)
        steal = self.derivative('cpu.total.steal', long(elements[8]), diamond.collector.MAX_COUNTER)
        guest = self.derivative('cpu.total.guest', long(elements[9]), diamond.collector.MAX_COUNTER)
        guest_nice = self.derivative('cpu.total.guest_nice', long(elements[10]), diamond.collector.MAX_COUNTER)

        total = sum([user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice])

        # Derivatives take one cycle to warm up
        if total != 0:
            self.publish('cpu.total.utilization.percent', (total - idle) / total * 100)
