'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel      

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        self.fanout=fanout

        controller = self.addSwitch('c1')
        for i in irange(1, fanout):
        	aggregate = self.addSwitch('a%s' % i)
        	##self.addLink( controller, aggregate, linkopts1('bw'), linkopts1('delay'), linkopts1('loss'), linkopts1('max_queue_size'), linkopts1('use_htb') )
        	self.addLink( controller, aggregate, **linkopts1)
        	for j in irange(1, fanout):
        		edge = self.addSwitch('e%s' % j)
        		##self.addLink( aggregate, edge, linkopts2('bw'), linkopts2('delay'), linkopts2('loss'), linkopts2('max_queue_size'), linkopts2('use_htb') )
        		self.addLink( aggregate, edge, **linkopts2)
        		for k in irange(1, fanout):
        			host = self.addHost('h%s' % k)
        			##self.addLink( edge, host, linkopts3('bw'), linkopts3('delay'), linkopts3('loss'), linkopts3('max_queue_size'), linkopts3('use_htb') )
        			self.addLink( edge, host, **linkopts3)
        		     
def simpleTest():
   	"Create network and run simple test"
   	linkopts1 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
   	linkopts2 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
   	linkopts3 = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
	topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)
   	net = Mininet(topo=topo)#, host=CPULimitedHost, link=TCLink)
   	net.start()
   	print "Testing network connectivity"
   	#net.pingAll() 
   	net.stop()

topos = { 'custom': ( lambda: CustomTopo() ) }

if __name__ == '__main__':
	setLogLevel('info')
	simpleTest()