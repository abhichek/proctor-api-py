import os

import boto3
import redis
from dotenv import load_dotenv
from github import Github
from openai import OpenAI

from claude_handler import ClaudeHandler

# Load environment variables
load_dotenv()


class AppServices:
    def __init__(self):
        # Initialize AWS clients
        # self.s3_client = boto3.client(
        #     "s3",
        #     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        #     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        #     region_name=os.getenv("AWS_REGION"),
        # )

        # self.sqs_client = boto3.client(
        #     "sqs",
        #     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        #     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        #     region_name=os.getenv("AWS_REGION"),
        # )

        # # Initialize GitHub client
        # self.github_client = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

        # # Initialize OpenAI client
        # self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize Redis client
        # self.redis_client = redis.Redis(
        #     host=os.getenv("REDIS_HOST"),
        #     port=int(os.getenv("REDIS_PORT")),
        #     password=os.getenv("REDIS_PASSWORD"),
        #     decode_responses=True,
        # )

        # Initialize Claude handler
        self.claude_handler = ClaudeHandler()

    def example_s3_operation(self, bucket_name, file_key):
        """Example S3 operation"""
        try:
            return self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
        except Exception as e:
            print(f"Error accessing S3: {e}")
            return None

    def example_sqs_operation(self, queue_url):
        """Example SQS operation"""
        try:
            return self.sqs_client.receive_message(
                QueueUrl=queue_url, MaxNumberOfMessages=1
            )
        except Exception as e:
            print(f"Error accessing SQS: {e}")
            return None

    def process_files_with_claude(self, file_paths):
        """Process files with Claude"""
        return self.claude_handler.process_files(file_paths)


def main():
    app = AppServices()

    # Example usage with three files
    file_paths = [
        "fd.txt",
        "code.ts",
        "swagger.json",
    ]

    app.process_files_with_claude(file_paths)


if __name__ == "__main__":
    main()
