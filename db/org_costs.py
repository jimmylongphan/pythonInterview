from datetime import date
from typing import Dict

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from collections import defaultdict

def db(sql: str):
  
  engine = sqlalchemy.create_engine('postgresql://coderpad:@/coderpad?host=/tmp/postgresql/socket')
  connection = engine.connect()
  Session = sessionmaker(bind=engine)
  session = Session()
  metadata = sqlalchemy.MetaData()
  metadata.reflect(bind=engine)
  result = session.execute(sqlalchemy.text(sql))
  return result

def slowest_warehouses_by_org() -> Dict[str, str]:
  org_sql = """
    SELECT *
    FROM organizations
  """
  query_sql = """
    SELECT *
    FROM historical_query_aggregates
  """
  orgs = db(org_sql)
  slowest = {}
  for org in orgs.fetchall():
    sql = query_sql + f" WHERE org_id = {org[0]!r} ORDER BY avg_total_elapsed_sec DESC LIMIT 1"
    for result in db(sql).fetchall():
      slowest[org[1]] = result[2]
  return slowest

def get_org_with_best_savings_no_sql() -> str:
  """
  Solve with either sql or another option
  best savings:
    estimated_credit_usage - actual_credit_usage
    savings per warehouse 

    aggregate for all warehouses for an org 

  cost_estimates table
    org_id, warehouse_id 

  ALGOS:
    query org_id, org_name from organizations 
      - save org_map[org_id] = org_name
      - only 1 sql request 

    keep track of highest savings org name 
    keep track of highest savings value 

    start with all cost_estimates 
      - iterate through all records 
      - estimated_credit_usage - actual_credit_usage
      - lookup org_name in the org_map
      - savings_map[org_name] += cost_savings 
      - if savings > highest_savings_value
        - update org_name

    result is the name of the org with highest cost savings
  """

  org_names = {}
  org_sql = """
    SELECT *
    FROM organizations
  """
  orgs = db(org_sql)
  for org in orgs.fetchall():
    org_names[org[0]] = org[1]

  highest_savings_org = ""
  highest_savings_value = 0
  savings_map = defaultdict(float)
  sql = """
    SELECT * FROM cost_estimates;
  """
  cost_estimates = db(sql)
  for cost_estimate in cost_estimates.fetchall():
    org_id = cost_estimate[0]
    org_name = org_names[org_id]
    actual_credit_usage = cost_estimate[4]
    estimated_credit_usage = cost_estimate[5]
    cost_savings = estimated_credit_usage - actual_credit_usage
    savings_map[org_name] += cost_savings

    if savings_map[org_name] > highest_savings_value:
      highest_savings_org = org_name
      highest_savings_value = savings_map[org_name]
  
  return highest_savings_org


