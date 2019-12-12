# -*- coding: utf-8 -*-

"""Classes for Route53 domains."""

import util


class DomainManager:
    """Manage a Route 53 domain."""

    def __init__(self, session):
        """Create DomainManager object."""
        self.session = session
        self.client = self.session.client("route53")

    def find_hosted_zone(self, domain):
        paginator = self.client.get_paginator("list_hosted_zones")
        for page in paginator.paginate():
            for zone in page["HostedZones"]:
                if domain.endswith(zone["Name"][:-1]):
                    return zone

        return None

    def create_s3_domain_record(self, zone, domain_name, endpoint):
        return self.client.change_resource_record_sets(
            HostedZoneId=zone["Id"],
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": domain_name,
                            "Type": "A",
                            "AliasTarget": {
                                "HostedZoneId": endpoint.zone,
                                "DNSName": endpoint.host,
                                "EvaluateTargetHealth": False
                            },
                        },
                    }
                ]
            },
        )
