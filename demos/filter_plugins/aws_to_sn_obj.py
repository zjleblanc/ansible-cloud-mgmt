class FilterModule(object):
  
  def filters(self):
    return { 
      "to_sn_vpc": self.convert_to_sn_vpc,
      "to_sn_subnet": self.convert_to_sn_subnet 
    }

  def convert_to_sn_vpc(self, vpc):
    return {
      "u_cidr_block": vpc['cidr_block'],
      "u_dhcp_options_id": vpc['dhcp_options_id'],
      "u_enable_dns_hostnames": vpc['enable_dns_hostnames'],
      "u_enable_dns_support": vpc['enable_dns_support'],
      "u_id": vpc['id'],
      "u_instance_tenancy": vpc['instance_tenancy'],
      "u_is_default": vpc['is_default'],
      "u_owner_id": vpc['owner_id'],
      "u_state": vpc['state'],
      "u_name": vpc['tags']['Name']
    }
  
  def convert_to_sn_subnet(self, subnet, vpc_sys_id):
    return {
      "u_assign_ipv6_address_on_creation": subnet["assign_ipv6_address_on_creation"],
      "u_availability_zone": subnet["availability_zone"],
      "u_availability_zone_id": subnet["availability_zone_id"],
      "u_available_ip_address_count": subnet["available_ip_address_count"],
      "u_cidr_block": subnet["cidr_block"],
      "u_default_for_az": subnet["default_for_az"],
      "u_enable_dns64": subnet["enable_dns64"],
      "u_id": subnet["id"],
      "u_ipv6_native": subnet["ipv6_native"],
      "u_map_customer_owned_ip_on_launch": subnet["map_customer_owned_ip_on_launch"],
      "u_map_public_ip_on_launch": subnet["map_public_ip_on_launch"],
      "u_owner_id": subnet["owner_id"],
      "u_enable_resource_name_dns_a_record": subnet["private_dns_name_options_on_launch"]["enable_resource_name_dns_a_record"],
      "u_enable_resource_name_dns_aaaa_record": subnet["private_dns_name_options_on_launch"]["enable_resource_name_dns_aaaa_record"],
      "u_hostname_type": subnet["private_dns_name_options_on_launch"]["hostname_type"],
      "u_state": subnet["state"],
      "u_subnet_arn": subnet["subnet_arn"],
      "u_subnet_id": subnet["subnet_id"],
      "u_name": subnet["tags"]["Name"],
      "u_vpc_id": subnet["vpc_id"],
      "u_vpc": vpc_sys_id
    }
