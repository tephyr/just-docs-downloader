#!/usr/bin/env python
#coding:utf-8
# Author: Andrew Ittner <projects@rhymingpanda.com>
# Created: 2015-04-07

import argparse
import json
import os.path
from   pprint import pformat
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
        self.__format_as_json = cli_args.json
        self.__username = cli_args.username
        self.__password = cli_args.password
        self.__use_auth = True if self.__username else False
        self.__verbose = cli_args.verbose
        
    
    def run(self):
        """Run download process."""
        # Build URL.
        url_all_docs_simple = self.__get_all_docs_URL()
        if self.__verbose:
            print("Getting all doc keys from {0}".format(url_all_docs_simple))

        response = None

        # Retrieve unfiltered _all_docs.
        try:
            response = requests.get(url_all_docs_simple,
                                    auth=(self.__username, self.__password) if self.__use_auth else None)
        except Exception as exc:
            # Fail out for any error
            print("Error occured while retrieving UNFILTERED _all_docs.")
            print(exc)
            return

        # Filter out design docs.
        doc_keys = self.__get_filtered_keys(response.json())

        # Retrieve filtered _all_docs.
        try:
            url_all_docs_full = self.__get_all_docs_URL(include_docs=True)
            if self.__verbose:
                print("Getting filtered docs from {0}".format(url_all_docs_full))
            
            response = requests.post(url_all_docs_full,
                                     auth=(self.__username, self.__password) if self.__use_auth else None,
                                     data=json.dumps(doc_keys))

            if self.__verbose and response.status_code != 200:
                print("Problem with this status code: {0}".format(response.status_code))

            # Write out as formatted JSON to output file.
            with open(self.__output, mode="w") as f:
                if self.__format_as_json:
                    f.write(pformat(response.json()))
                else:
                    #print(response.encoding)
                    f.write(response.text.encode("utf8"))

        except Exception as exc:
            # Fail out for any error
            print("Error occured while retrieving FILTERED _all_docs.")
            print(exc)
            return
        
    def __get_all_docs_URL(self, include_docs=False):
        parsed_url = urlparse.urlsplit(self.__server_url)
        complete_url = (parsed_url[0], parsed_url[1],
                        "{0}/{1}".format(self.__db_name, "_all_docs"),
                        "", "include_docs=true" if include_docs else "",
                        "")
        return urlparse.urlunparse(complete_url)
    
    def __get_filtered_keys(self, results):
        """Get filtered keys from _all_docs result."""
        # Find all documents that do NOT start with "_design/".
        keys = [doc["key"] for doc in results.get("rows", []) if not doc["key"].startswith("_design/")]

        if self.__verbose:
            print("Total rows (original): {0}; filtered rows: {1}".format(
                results.get("total_rows", "?"),
                len(keys)
            ))

        return {"keys": keys}

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
    parser.add_argument("--json", action="store_true",
                        help="Write as formatted JSON.")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose")
    args = parser.parse_args()
    
    jdd = JustDocsDownloader(args)
    jdd.run()
    

if __name__=='__main__':
    run()
