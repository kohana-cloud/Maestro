import boto3
import os
from botocore.config import Config
from .aws_query import AWS_LIST_RESOURCE_QUERIES, run_raw_operation

ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXX"
SECRET_KEY="XXXXXXXXXXXXXXXXXXXXX"

SERVICE_BLACKLIST= ['alexaforbusiness', 'kinesis-video-media']

class AWS_Session():
	def __init__(self):
		#See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#guide-credentials for more details
		self.aws_region_name = os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1' 
		self.session = boto3.Session(
				aws_access_key_id=ACCESS_KEY,
				aws_secret_access_key=SECRET_KEY,
				region_name=self.aws_region_name,
		)
		
		print("AWS_Session({%s}) bound in region({%s})" % (self.session.profile_name, self.session.region_name))

	def get_services_names(self):
		"""Return a list of available service names e.g. 's3' or 'ec2'."""
		return [service for service in sorted(self.session.get_available_services()) if service not in SERVICE_BLACKLIST]

	def get_region_list(self):
		print("* Getting region names", flush=True)
		EC2_REGIONS = set([region['RegionName'] for region in self.session.client("ec2").describe_regions()['Regions']])
		S3_REGIONS = set(self.session.get_available_regions('s3'))
		ALL_REGIONS = sorted(EC2_REGIONS | S3_REGIONS)
		return ALL_REGIONS

	def get_regional_sessions_using_root_user(self):
		ALL_REGIONS = self.get_region_list()
		print("* Initializating %d regional session" % len(ALL_REGIONS))
		sessions = {region: boto3.Session(
			aws_access_key_id=ACCESS_KEY,
			aws_secret_access_key=SECRET_KEY,
			region_name=region,
			) for region in ALL_REGIONS
		}
		if sessions[ALL_REGIONS[0]].get_credentials() is None:
			print("WARNING: No credentials available for listing. ")
		return sessions

	def get_regional_sessions(self, credentials):
		ALL_REGIONS = self.get_region_list()
		print("* Initializating %d regional session" % len(ALL_REGIONS))
		sessions = {region: boto3.Session(
			aws_access_key_id=credentials['AccessKeyId'],
			aws_secret_access_key=credentials['SecretAccessKey'],
			aws_session_token=credentials['SessionToken'],
			region_name=region,
			) for region in ALL_REGIONS
		}
		if sessions[ALL_REGIONS[0]].get_credentials() is None:
			print("WARNING: No credentials available for listing. ")
		return sessions	

	#FIXME
	def get_sts_role_credentials(self): 
		sts_client = boto3.client('sts', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
		assumed_role_object=sts_client.assume_role(
			RoleArn="arn:aws:iam::032622136258:role/KohanaAdmin",
			RoleSessionName="AssumeRoleSession1"
		)
		credentials=assumed_role_object['Credentials']
		print(credentials)
		return credentials

	
	def get_all_services(self):
		all_services = self.get_services_names()
		sts_credentials = self.get_sts_role_credentials()
		regional_sessions = self.get_regional_sessions(sts_credentials)
		result = {}


		for service in all_services:
			method_to_call = AWS_LIST_RESOURCE_QUERIES.get(service) #TODO: snakecase
			if method_to_call is None:
				continue
			result[service] = {}
			for region, session in regional_sessions.items():
				if region == 'ap-east-1':
					continue
				handler = session.client(
					service,
					#endpoint_url="https://sts.{}.amazonaws.com".format(region),
					config=Config(
						retries={
							"max_attempts": 10,
							'mode': 'standard'
						}
					),
				)
				print("Enabling (%s,%s)" % (service, region))
				result[service][region] = run_raw_operation(handler, method_to_call)
				
		return result


	def get_resources_taggingapi(self, region="us-west-1"):
		tagapi = self.session.client('resourcegroupstaggingapi', region_name=region)
		resp = tagapi.get_resources(ResourcesPerPage=2)
		for resource in resp['ResourceTagMappingList']:
			print("Resource: ", resource)
		return resp

	def get_all_rds_instances(self):
		return self.session.client('rds').describe_db_instances()

	def get_all_buckets(self):
		s3 = self.session.resource('s3')
		return s3.buckets.all()


