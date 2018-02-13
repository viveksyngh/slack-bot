# This is just as test comment

from fabric.api import *

class ParallelCommands():
    def __init__(self, **args):
        self.hosts = args['hosts']
        self.command = args['command']

    @parallel(pool_size=10) # Run on as many as 10 hosts at once
    def parallel_exec(self):
        return run(self.command)

    def capture(self):
        with settings(hide('running', 'commands', 'stdout', 'stderr')):
            stdout = execute(self.parallel_exec, hosts=self.hosts)
        return stdout

hosts = ['vivek@localhost']
command = 'uname -a'

instance = ParallelCommands(hosts=hosts, command=command)
output = instance.capture()

print output['vivek@localhost']