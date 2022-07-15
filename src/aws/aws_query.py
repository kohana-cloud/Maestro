AWS_LIST_RESOURCE_QUERIES = {
	'ec2': 'describe_instances',
	'rds': 'describe_db_instances',
	#'dynamodb': 'tables',
	'logs': 'describe_log_groups',
	#'s3': 'buckets'
}


def run_raw_operation(klass, method, parameters=None):
	if parameters is None:
		return getattr(klass, method)()
	else:
		return getattr(klass, method)(*parameters)