class AWS_SVC_BASE():
	aws_config = Config(
        retries=dict(
            total_max_attempts=25,
            mode='adaptive'
        ),
        max_pool_connections=MAX_POOL_CONNECTIONS,            
    )

	def __init__(self, session):
		self.session = session
