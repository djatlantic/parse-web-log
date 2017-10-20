#!/usr/bin/env python

import argparse
import collections
import os
import re
import string
import sys

class ParseWebLogFile():
    """
    Class to parse the log file and print out stats for each day
    1. What are the number of requests served by day?  
    2. What are the 3 most frequent User Agents by day?
    3. What is the ratio of GET's to POST's by OS by day?
    """

    webstats = collections.defaultdict(dict)
    log = ""
           
    def __init__(self, logFile):
        self.log = logFile

    
    def parseFile(self):

	with open(self.log) as f:
    	   for line in f:
        	m = re.match(r'.*\[([0-9]{2}\/[A-Z][a-z]+\/[0-9]{4}):[0-9]+:.*"([A-Z]{3,}).*"(.*)"$', line)
        	if m.group(1) not in self.webstats:
            	    self.webstats[m.group(1)]['agent'] = {}
            	    self.webstats[m.group(1)]['agent'][m.group(3)] = 1
                    self.webstats[m.group(1)]['type'] = {}
                    self.webstats[m.group(1)]['type'][m.group(2)] = 1
                else:
                    if m.group(3) in self.webstats[m.group(1)]['agent']:
                        self.webstats[m.group(1)]['agent'][m.group(3)] += 1
                    else:
                        self.webstats[m.group(1)]['agent'][m.group(3)] = 1

                    if m.group(2) in self.webstats[m.group(1)]['type']:
                        self.webstats[m.group(1)]['type'][m.group(2)] += 1
                    else:
                        self.webstats[m.group(1)]['type'][m.group(2)] = 1

    def printOutput(self, all):
	for date, stats in self.webstats.iteritems():

  	    if all:
	        m = re.match(r'[0-9]{2}\/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\/[0-9]{4}$', date)

   		if m: 
    	    	    print "Date: {0}".format(date)
            	else:
    	    	    #print "Date: {0}".format(date)
		    continue 
	    else:
    	    	print "Date: {0}".format(date)

	    total = 0
            post = 0
            get = 0
    
	    for action,value in stats['type'].iteritems():
                if action == 'GET':
                    get = value
                elif action == 'POST':
                    post = value

                total += value

            print "Total requests: {0}".format(str(total))
	    print "Top 3 most frequent User Agents for {0}:".format(date) 
            count = 0
            for agent,agentCount in sorted(stats['agent'].iteritems(), key=lambda (k,v): (v,k), reverse=True):
                count += 1
                print "{0}. {1}, counts: {2}".format(count, agent, agentCount)

                if count == 3:
                    break

            if post != 0:
                print "GET to POST ratio:  {0}".format(str(get/post))


            print "#########################"

def main():
    parser = argparse.ArgumentParser(description="Parse web log and display some stats")
    parser.add_argument('--all', dest='all', action='store_false', help="display all stats including bad date format log entries")
    parser.add_argument('--log', dest='log', required=True, help="pull path to log file")

    args = parser.parse_args()

    if not os.path.isfile(args.log):
        print "FATAL: Could not file {0}".format(args.log)
	sys.exit(1)


    stats = ParseWebLogFile(args.log) 
    stats.parseFile()
    stats.printOutput(args.all)

if __name__ == '__main__':
        main()
   
