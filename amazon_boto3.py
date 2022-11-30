import boto3
import botocore
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
)



db = session.resource('dynamodb')

print(db)

news_corpus_table = db.Table("news-corpus")

def update_db(news_site, day, month, year, headlines):
        """
        Takes a list of headlines and assigns it to a date
        news_site: string
        date: string
        headline: list
        """
        try:
            response = news_corpus_table.update_item(
                Key={'news-source': news_site},
                UpdateExpression="SET #year.#month.#day = :h",
                ExpressionAttributeValues={
                    ":h": headlines
                },
                ExpressionAttributeNames= {
                    "#year": year,
                    "#month": month,
                    "#day": day
                },
                ReturnValues="UPDATED_NEW"
            )
        except botocore.exceptions.ClientError as err:
            return err.response['Error']['Code'], err.response['Error']['Message']
            pass
        else:
            return response['Attributes']







# class Movies:
#     """Encapsulates an Amazon DynamoDB table of movie data."""
#     def __init__(self, dyn_resource):
#         """
#         :param dyn_resource: A Boto3 DynamoDB resource.
#         """
#         self.dyn_resource = dyn_resource
#         self.table = None

#     def create_table(self, table_name):
#         """
#         Creates an Amazon DynamoDB table that can be used to store movie data.
#         The table uses the release year of the movie as the partition key and the
#         title as the sort key.

#         :param table_name: The name of the table to create.
#         :return: The newly created table.
#         """
#         try:
#             self.table = self.dyn_resource.create_table(
#                 TableName=table_name,
#                 KeySchema=[
#                     {'AttributeName': 'year', 'KeyType': 'HASH'},  # Partition key
#                     {'AttributeName': 'title', 'KeyType': 'RANGE'}  # Sort key
#                 ],
#                 AttributeDefinitions=[
#                     {'AttributeName': 'year', 'AttributeType': 'N'},
#                     {'AttributeName': 'title', 'AttributeType': 'S'}
#                 ],
#                 ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
#             self.table.wait_until_exists()
#         except ClientError as err:
#             logger.error(
#                 "Couldn't create table %s. Here's why: %s: %s", table_name,
#                 err.response['Error']['Code'], err.response['Error']['Message'])
#             raise
#         else:
#             return self.table

# movies_db = Movies(db)
# print(movies_db.create_table("movies"))
