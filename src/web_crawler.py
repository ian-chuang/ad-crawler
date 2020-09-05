
from automation import CommandSequence, TaskManager
import csv


sites = []

with open('/home/ian/Downloads/top-1m.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        a = row[0].split(',')
        sites.append('http://' + a[1])
        if a[0] == '100':
            break

# The list of sites that we wish to crawl
NUM_BROWSERS = 5

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record Navigations
    #browser_params[i]['navigation_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True

    browser_params[i]["ublock-origin"] = True
    print (browser_params[i]["ublock-origin"])
    # Record the callstack of all WebRequests made
    #browser_params[i]['callstack_instrument'] = True
# Launch only browser 0 headless
browser_params[0]['display_mode'] = 'headless'

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence.CommandSequence(
        site, reset=True,
        callback=lambda success, val=site:
        print("CommandSequence {} done".format(val)))

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=60)

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
