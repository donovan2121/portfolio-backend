import boto3


def create_visitors_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')


    table = dynamodb.create_table(
        TableName = 'Visitors',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 2
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='Visitors')
    assert table.table_status == 'ACTIVE'

    return table

if __name__ == '__main__':
    visitors_table = create_visitors_table()
    print("Table status:", visitors_table.table_status)
