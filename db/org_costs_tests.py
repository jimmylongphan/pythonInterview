
from datetime import date, datetime
import unittest


from main import db, slowest_warehouses_by_org, get_org_with_best_savings_no_sql

class UnitTestDb(unittest.TestCase):
  def test_db_executes(self):
    sql = "select * from organizations limit 1"
    results = db(sql)
    # print(f"test_db_executes {results}")
    assert results
  
class IntegrationTest(unittest.TestCase):
  def test_gets_slowest_warehouse_by_org(self):
    expected = {
      'Allbirds': '452ba4d2-1768-4937-9123-e40b739a9a03',
      "Nike": "38525c31-c193-4977-ac22-7c6360a3d915",
      "Adidas": "e0a982a5-e009-4ed1-aacb-561895aa5129",
      "Converse": "d6195907-7660-401a-af6d-7d2868eef591",
    }
    results = slowest_warehouses_by_org()
    # print(f"test_gets_slowest_warehouse_by_org {results}")
    assert results == expected

  def test_get_org_with_best_savings(self):
    results = get_org_with_best_savings_no_sql()
    print(f"test_get_org_with_best_savings {results}")
    assert results == 'Allbirds'

if __name__ == '__main__':
    unittest.main()

