#!/usr/bin/env python
#coding:utf-8
# Author: Andrew Ittner <projects@rhymingpanda.com>
# Created: 2015-04-07

import argparse
import json
import os.path
import urlparse

# 3rd-party
import requests

########################################################################
class JustDocsDownloader(object):
    """Download only the documents from a CouchDB database."""

    #----------------------------------------------------------------------
    def __init__(self, cli_args):
        self.__server_url = cli_args.serverurl
        self.__db_name = cli_args.dbname
        self.__output = os.path.expanduser(cli_args.output)
        self.__username = cli_args.username
        self.__password = cli_args.password
        self.__use_auth = True if self.__username else False
        
    
    def run(self):
        print(self.__server_url, self.__db_name, self.__output)
        print(self.__username, self.__use_auth)

        # Build URL.
        url_all_docs = self.__get_all_docs_URL()
        print(url_all_docs)
        response = None

        # Retrieve unfiltered _all_docs.
        try:
            if (self.__use_auth):
                response = requests.get(url_all_docs, auth=(self.__username, self.__password))
            else:
                response = requests.get(url_all_docs)

            print(response.status_code)
            with open(self.__output, mode="w") as f:
                f.write(response.text)

        except Exception as exc:
            # Fail out for any error
            print("Error occured while retrieving unfiltered _all_docs.")
            print(exc)
            return

        # Filter out design docs.
        # Retrieve filtered _all_docs.
        # Save to output.
        
    def __get_all_docs_URL(self):
        parsed_url = urlparse.urlsplit(self.__server_url)
        complete_url = (parsed_url[0], parsed_url[1],
                        "{0}/{1}".format(self.__db_name, "_all_docs"),
                        "", "")
        return urlparse.urlunsplit(complete_url)
    
def run():
    parser = argparse.ArgumentParser(description="Download docs from CouchDB.")
    parser.add_argument("--serverurl", required=True,
                        help="Full URL to CouchDB *server* (including name/password if using basic authentication).")
    parser.add_argument("--dbname", required=True,
                        help="Database name.")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--output",
                        help="Full path to output file.")
    args = parser.parse_args()
    
    jdd = JustDocsDownloader(args)
    jdd.run()
    

if __name__=='__main__':
    run()
