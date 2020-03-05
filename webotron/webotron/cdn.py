# -*- coding: utf-8 -*-

"""Classes for CloudFront distributions."""

import uuid

class DistributionManager:
    def __init__(self, session):
        self.session = session
        self.client = self.session.client("cloudfront")

    def find_matching_dist(self, domain_name):
        """Find a dist maching domain_name"""
        paginator = self.client.get_paginator('list_distributions')
        for page in paginator.paginate():
            for dist in page["DistributionList"]["Items"]:
                for alias in dist["Aliases"].get("Items", []):
                    if alias == domain_name:
                        return dist

        return None

    def create_dist(self, domain_name, cert):
        """Create a dist for domain_name using cert"""
        origin_id = 'S3-' + domain_name
        result = self.client.create_distribution(
            DistributionConfig={
                'Comment': '',
                'CallerReference': str(uuid.uuid4()),
                'Aliases': {
                    'Quantity': 1,
                    'Items': [domain_name]   
                },
                'DefaultRootObject': 'index.html',
                'Enabled': True,
                'Origins': {
                    'Quantity': 1,
                    'Items': [{
                        'Id': origin_id,
                        'DomainName': f"{domain_name}.s3.amazonaws.com",
                        "S3OriginConfig": {
                            "OriginAccessIdentity": ''
                        }
                    }]
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': origin_id,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners': {
                        'Quantity': 0,
                        'Enabled': False
                    },
                    'ForwardedValues': {
                        'Cookies': { 'Forward': 'all' } ,
                        'Headers': { 'Quantity': 0 },
                        'QueryString': False,
                        'QueryStringCacheKeys': {'Quantity': 0},
                    },
                    'DefaultTTL': 86400,
                    'MinTTL': 3600,
                },
                'ViewerCertificate': {
                    'ACMCertificateArn': cert['CertificateArn'],
                    'SSLSupportMethod': 'sni-only',
                    'MinimumProtocolVersion': 'TLSv1.1_2016'
                },
                'CustomErrorResponses': {
                    'Quantity': 1,
                    'Items': [{
                        'ErrorCode': 403,
                        'ResponsePagePath': '/index.html',
                        'ResponseCode': '200'
                    }]
                }
            }
        )

        return result['Distribution']

    def await_deploy(self, dist):
        """Wait for a dist to be deployed"""
        waiter = self.client.get_waiter('distribution_deployed')
        waiter.wait( 
            Id=dist["Id"],
            WaiterConfig={
                'Delay': 30,
                'MaxAttempts': 50
            }
        )
        pass