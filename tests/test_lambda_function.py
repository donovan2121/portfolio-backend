import boto3
from moto import mock_dynamodb
import unittest
from botocore.exceptions import ClientError
import lambda_function

@mock_dynamodb
class TestDBFunctions(unittest.TestCase):

    def setUp(self):
        """ 
        Create database resource and mock table
        """
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        from portfolio_table import create_visitors_table
        self.table = create_visitors_table(self.dynamodb)


    def tearDown(self):
        """
        Delete database resource and mock table
        """
        self.table.delete()
        self.dynamodb=None
    
    def test_table_exists(self):
        """
        Test if our mock table is ready
        """
        self.assertIn('Visitors', self.table.name)

    def test_post_visitors(self):
        from lambda_function import saveVisitors, buildResponse
        post_visitors = {
            "id": "101",
            "visitorsCount": 101
        }
        result = saveVisitors(post_visitors, self.dynamodb)
        self.assertEqual(200, result['statusCode'])

    def test_get_visitors(self):
        from lambda_function import getVisitors, saveVisitors, buildResponse
        post_visitors = {
            "id": "101",
            "visitorsCount": 1
        }
        saveVisitors(post_visitors, self.dynamodb) 
        # check if it returns correct object from db
        result = getVisitors('101',self.dynamodb)
        # self.assertEqual('101', result['id'])
        self.assertEqual(200, result['statusCode'])

    def test_patch_visitors(self):
        from lambda_function import saveVisitors, modifyVisitors, buildResponse
        post_visitors = {
            "id": "101",
            "visitorsCount": 1
        }
        saveVisitors(post_visitors, self.dynamodb) 
        result = modifyVisitors("101", "visitorsCount", 20, self.dynamodb)
        self.assertEqual(200, result['statusCode'])


if __name__ == '__main__':
    unittest.main()