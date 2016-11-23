from pysnmp.entity.rfc3413.oneliner import cmdgen

class F5Pools:

    pool_oids = { }
    pools = '1.3.6.1.4.1.3375.2.2.5'
    pool_stat = pools + '.2'
    pool_entry = pool_stat + '.3.1'
    pool_stat_name = pool_entry + '.1'
    pool_stat_total_connections = pool_entry + '.7'
    pool_stat_current_connections = pool_entry + '.8'
    pool_stat_packets_in = pool_entry + '.2'
    pool_stat_packets_out = pool_entry + '.4'
    pool_stat_bits_in = pool_entry + '.3'
    pool_stat_bits_out = pool_entry + '.5'
    pool_stat_total_requests = pool_entry + '.30'

    community = ""
    host = ""
    port = 0

    def __init__(self,community,host,port):
        self.community = community
        self.host = host
        self.port = port

    def get_metrics(self):
        self.get_single_metric(self.pool_stat_total_connections)
        self.get_single_metric(self.pool_stat_current_connections)
        self.get_single_metric(self.pool_stat_packets_in)
        self.get_single_metric(self.pool_stat_packets_out)
        self.get_single_metric(self.pool_stat_bits_in)
        self.get_single_metric(self.pool_stat_bits_out)
        self.get_single_metric(self.pool_stat_total_requests)

    def get_single_metric(self,metric):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            metric
        )
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex) - 1] or '?'
                )
                      )
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        pool_id = str(name).replace(metric, "")
                        self.pool_oids[pool_id].append(str(val))

    def get_pools(self):
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget((self.host, self.port)),
            self.pool_stat_name
        )

        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
            else:
                for varBindTableRow in varBindTable:
                    for name, val in varBindTableRow:
                        pool_id = str(name).replace(self.pool_stat_name,"")
                        self.pool_oids[pool_id] = [str(val)]

    def print_pool_names(self):
        for k,v in self.pool_oids.iteritems():
            print "bigip_pool," "host=" + self.host + \
                  ",pool=" + v[0]  + \
                  " total_connections=" + v[1] + \
                  ",current_connections=" + v[2] + \
                  ",packets_in=" + v[3] + \
                  ",packets_out=" + v[4] + \
                  ",bits_in=" + v[5] + \
                  ",bits_out=" + v[6] + \
                  ",total_requests=" + v[7]

f5_metrics = F5Pools('public','localhost',161)
f5_metrics.get_pools()
f5_metrics.get_metrics()
f5_metrics.print_pool_names()