#!/usr/bin/env python3
#
# Program : report.py
# Version : 0.1
# Date    : Jun 15, 2021
# Author  : Jan Souza
# Brief   : External report (csv) for Kube Bench
#

import json
import csv
import os
import argparse
import jmespath


def processCSV(files):
    head_ = []
    head_.append('hostname')

    head_info = []
    head_info.append('version')
    head_info.append('detected_version')
    head_info.append('text')
    head_info.append('node_type')

    head_test = []
    head_test.append('section')
    head_test.append('type')
    head_test.append('pass')
    head_test.append('fail')
    head_test.append('warn')
    head_test.append('info')
    head_test.append('desc')

    head_result = []
    head_result.append('test_number')
    head_result.append('test_desc')
    head_result.append('audit')
    head_result.append('AuditEnv')
    head_result.append('AuditConfig')
    head_result.append('type')
    head_result.append('remediation')
    head_result.append('status')
    head_result.append('scored')
    head_result.append('IsMultiple')
    head_result.append('expected_result')

    head = head_ + head_info + head_test + head_result

    csv_data = []
    for file in files:
        with open(file) as json_file:
            import_data = json.load(json_file)
            # print(import_data)

            controls = import_data['Controls']
            for server_node in controls:

                tests = server_node['tests']
                for test in tests:

                    results = test['results']
                    for result in results:
                        csv_coll = []

                        hostname = os.path.basename(file)
                        hostname = hostname.split('-')[0]
                        csv_coll.append(hostname)

                        for item in head_info:
                            value = jmespath.search(item, server_node)
                            csv_coll.append(value)

                        for item in head_test:
                            value = jmespath.search(item, test)
                            csv_coll.append(value)

                        for item in head_result:
                            value = jmespath.search(item, result)
                            csv_coll.append(value)

                        # append row
                        csv_data.append(csv_coll)

    if csv_data:
        with open(os.path.dirname(file) + '/kube-bench-report.csv', 'w', encoding='UTF8', newline='\n') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(head)
            for row in csv_data:
                writer.writerow(row)


def get_args():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(description="Report")
    parser._optionals.title = "Options"

    parser.add_argument('-f', required=True, help='Directory', dest='dir_process', type=str)

    return parser


def main():
    # Handling arguments
    parser = get_args()
    args = parser.parse_args()

    dir_process = args.dir_process
    print("dir_process=" + dir_process)

    if (os.path.isdir(dir_process)):
        files = []
        for r, d, f in os.walk(dir_process):
            for file in f:
                if '.json' in file:
                    files.append(os.path.join(r, file))

        processCSV(files)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
