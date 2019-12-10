from urllib.request import urlopen
from urllib.parse import quote_plus
import json
import sys

fields = [
    ["realtime_tx_bytes",   ""],
    ["lte_rsrp",            "Reference Signal Received Power"],
    ["lte_rsrq",            "Reference Signal Received Quality"],
    ["lte_rssi",            "Receive Strength Signal Indicator"],
    ["lte_band",            "LTE frequency band"],
    ["signalbar",           "Signal bars"],
    ["realtime_tx_bytes",   "Realtime transmitted bytes"],
    ["realtime_rx_bytes",   "Realtime received bytes"],
    #["realtime_time",       "Realtime time"],
    ["realtime_tx_thrpt",   "Realtime transmitted throughput"],
    ["realtime_rx_thrpt",   "Realtime received throughput"],
    ["monthly_tx_bytes",    "Monthly transmitted bytes"],
    ["monthly_rx_bytes",    "Monthly received bytes"],
    #["monthly_time",        "Time of month"],
    ["total_tx_bytes",      "Total transmitted bytes"],
    ["total_rx_bytes",      "Total received bytes"],
]

# Whether to show configuration data, or just values.
do_config = len(sys.argv) > 1 and sys.argv[1] == "config"

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
   
values = get_modem_json([field[0] for field in fields])

if do_config:
    print("graph_title ZTE MF823 4g modem")
    print("graph_category:  network")

for ident, label in fields:
    if do_config:
        print("{}.label {}".format(ident, label))
        
    print("{}.value {}".format(ident, values[ident]))
