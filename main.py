from supermarket import Supermarket
import time

aldi=Supermarket(120)
for i in range(120):
    time.sleep(0.1)
    aldi.add_new_customers()
    aldi.print_customers()
    aldi.next_minute()
    aldi.remove_exitsting_customers()
    
aldi.write_all_locations_to_csv()   

    