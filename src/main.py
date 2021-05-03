#!/usr/bin/env python3
"""
Main
"""
# coding: utf-8

import csv

PLANS = 'csv/plans.csv'
ZIPS = 'csv/zips.csv'
SLCSP = 'csv/slcsp.csv'
OUTPUT = 'csv/slcsp_out.csv'

def slcsp_csv():
    """slcsp"""
    plans = {}
    for plan in csv.DictReader(open(PLANS, 'r')):
        code = '{state} {rate_area}'.format(**plan)
        if plan.get('metal_level') == 'Silver':
            plans.setdefault(code, []).append(plan['rate'])

    zips = {}
    for zcode in csv.DictReader(open(ZIPS, 'r')):
        code = '{state} {rate_area}'.format(**zcode)
        zips.setdefault(zcode['zipcode'], []).append(code)

    rates = []
    slcsp = csv.DictReader(open(SLCSP, 'r'))
    for row in slcsp:
        zipcode = zips.get(row['zipcode']) or []
        if len(set(zipcode)) == 1: # if not 1, multiple rate areas; ambiguous
            plan_rates = list(set(float(pr) for pr in (plans.get(zipcode[0]) or [])))
            plan_rates.sort()
            if len(plan_rates) > 1: # need at least 2 silver plans
                row['rate'] = plan_rates[1]

        rates.append(row)

    output = open(OUTPUT, 'w')
    writer = csv.DictWriter(output, slcsp.fieldnames)
    writer.writeheader()
    writer.writerows(rates)
    output.close()

    print(open(OUTPUT, 'r').read())

if __name__ == "__main__":
    slcsp_csv()
