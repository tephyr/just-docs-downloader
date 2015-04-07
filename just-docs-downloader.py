#!/usr/bin/env python
#coding:utf-8
# Author: Andrew Ittner <projects@rhymingpanda.com>
# Created: 2015-04-07

import argparse

########################################################################
class JustDocsDownloader(object):
    """Download only the documents from a CouchDB database."""

    #----------------------------------------------------------------------
    def __init__(self, cli_args):
        pass
        
    
    def run(self):
        pass
    
def run():
    parser = argparse.ArgumentParser(description="Download docs from CouchDB.")
    parser.add_argument("url", 
                        help="Full URL to CouchDB database (including name/password if using basic authentication).")
    parser.add_argument("output",
                        help="Full path to output file.")
    args = parser.parse_args()
    
    jdd = JustDocsDownloader(args)
    jdd.run()
    

if __name__=='__main__':
    run()
