#!/usr/bin/env python3
from urllib.request import urlopen
from urllib.parse import quote_plus
import json
import sys
import hashlib

# Whether to show configuration data, or just values.
do_config = len(sys.argv) > 1 and sys.argv[1] == "config"

# Munin graph details
graphs = [
    {
        "multigraph": "lte_signal",
        "graph_category": "lte",
        "graph_title": "LTE connection",
        "graph_info": "LTE Connection signal statistics",
        "fields": [
            ["lte_rsrp",    "Reference Signal Received Power"],
            ["lte_rsrq",    "Reference Signal Received Quality"],
            ["lte_rssi",    "Received Strength Signal Indicator"],
            ["tx_power",    "tx_power"],
            ["signalbar",   "Signal bars"],
        ]
    },
    {
        "multigraph": "lte_misc",
        "graph_category": "lte",
        "graph_title": "LTE miscellaneous",
        "graph_info": "LTE miscellaneous details",
        "fields": [
            ["lte_band",        "LTE frequency band"],
            ["lac_code",        "Location Area Code"],
            ["cell_id",         "Cell ID"],
            ["wan_ipaddr",      "WAN IP"],
            ["lte_pci",         "lte_pci"],
            ["enodeb_id",       "enodeb_id"],
            ["network_type",    "network_type"],
            ["network_provider_fullname", "network_provider_fullname"],
        ]
    },
    {
        "multigraph": "lte_throughput",
        "graph_category": "lte",
        "graph_title": "LTE throughput",
        "graph_info": "LTE throughput data statistics",
        
        "fields": [
            ["realtime_tx_thrpt", "Realtime upload throughput"],
            ["realtime_rx_thrpt", "Realtime download throughput"],
        ]
    },
    {
        "multigraph": "lte_realtime",
        "graph_category": "lte",
        "graph_title": "LTE realtime",
        "graph_info": "LTE Realtime data statistics",
        
        "fields": [
            ["realtime_tx_bytes", "Realtime uploaded bytes"],
            ["realtime_rx_bytes", "Realtime downloaded bytes"],
        ]
    },
    {
        "multigraph": "lte_monthly_usage",
        "graph_category": "lte",
        "graph_title": "LTE monthly data usage",
        "graph_info": "LTE monthly data usage statistics",
        
        "fields": [
            ["monthly_tx_bytes",   "Monthly uploaded bytes"],
            ["monthly_rx_bytes",   "Monthly downloaded bytes"],
        ]
    },
    {
        "multigraph": "lte_total_usage",
        "graph_category": "lte",
        "graph_title": "LTE total data usage",
        "graph_info": "LTE total data usage statistics",
        
        "fields": [
            ["total_tx_bytes",     "Total uploaded bytes"],
            ["total_rx_bytes",     "Total downloaded bytes"],
        ]
    }
]

def get_modem_json(fields):
    
    # Modem its IP address. Can't change without hardware modding.
    host = "192.168.0.1"
    
    
    param = quote_plus(",".join(fields))
    url = "http://{}/goform/goform_get_cmd_process?isTest=false&cmd={}&multi_data=1"
    
    url = url.format(host, param)
  
    request = urlopen(url);
    
    if request.getcode() != 200:
        print("fatal: host returned non 200 reponse", file=sys.stderr)
        exit(1)
    
    response = request.read()
    
    obj = json.loads(response)
    
    return obj
   

fields = []
for graph in graphs:
    fields += [field[0] for field in graph["fields"]]   
   
values = get_modem_json(fields)

for graph in graphs:
    print("multigraph {}".format(graph["multigraph"]))

    if do_config:
        print("graph_title {}".format(graph["graph_title"]))
        print("graph_category {}".format(graph["graph_category"]))
        print("graph_info {}".format(graph["graph_info"]))
        print("graph_args --base 1000")

    for ident, label in graph["fields"]:
        
        value = values[ident]
        
        try:
            value = int(value)
        except:
            # Get a fairly unique representation.
            value = str(abs(hash(value)))[0:4]
            
        if do_config:
            print("{}.label {}".format(ident, label))
            print("{}.graph yes".format(ident))
        else:        
            print("{}.value {}".format(ident, value))
