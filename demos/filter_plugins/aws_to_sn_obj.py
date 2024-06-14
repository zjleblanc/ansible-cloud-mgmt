class FilterModule(object):
  
  def filters(self):
    return { 
      "to_sn_vpc": self.convert_to_sn_vpc,
      "to_sn_subnet": self.convert_to_sn_subnet,
      "to_sn_security_group": self.convert_to_sn_security_group,
      "to_sn_ec2": self.convert_to_sn_ec2
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

  def convert_to_sn_security_group(self, sg, vpc_sys_id):
    return {
      "u_name": sg["group_name"],
      "u_id": sg["group_id"],
      "u_owner_id": sg["owner_id"],
      "u_description": sg["description"],
      "u_vpc": vpc_sys_id
    }
  
  def convert_to_sn_ec2(self, instance, vpc_sys_id, subnet_sys_id):
    return {
      "u_ami_launch_index": instance["ami_launch_index"],
      "u_architecture": instance["architecture"],
      "u_boot_mode": instance["boot_mode"],
      "u_capacity_reservation_preference": instance["capacity_reservation_specification"]["capacity_reservation_preference"],
      # "u_client_token": instance["client_token"],
      "u_core_count": instance["cpu_options"]["core_count"],
      "u_threads_per_core": instance["cpu_options"]["threads_per_core"],
      "u_current_instance_boot_mode": instance["current_instance_boot_mode"],
      "u_ebs_optimized": instance["ebs_optimized"],
      "u_ena_support": instance["ena_support"],
      # "u_enabled": instance["enabled"],
      # "u_configured": instance["configured"],
      "u_hypervisor": instance["hypervisor"],
      "u_image_id": instance["image_id"],
      "u_instance_id": instance["instance_id"],
      "u_instance_type": instance["instance_type"],
      "u_key_name": instance["key_name"],
      "u_launch_time": instance["launch_time"],
      "u_auto_recovery": instance["maintenance_options"]["auto_recovery"],
      # "u_http_endpoint": instance["http_endpoint"],
      # "u_http_protocol_ipv6": instance["http_protocol_ipv6"],
      # "u_http_put_response_hop_limit": instance["http_put_response_hop_limit"],
      # "u_http_tokens": instance["http_tokens"],
      # "u_instance_metadata_tags": instance["instance_metadata_tags"],
      # "u_state": instance["state"],
      # "u_state": instance["state"],
      "u_availability_zone": instance["placement"]["availability_zone"],
      "u_group_name": instance["placement"].get("group_name", None),
      "u_tenancy": instance["placement"]["tenancy"],
      "u_platform_details": instance["platform_details"],
      "u_private_dns_name": instance["private_dns_name"],
      "u_enable_resource_name_dns_a_record": instance["private_dns_name_options"]["enable_resource_name_dns_a_record"],
      "u_enable_resource_name_dns_aaaa_record": instance["private_dns_name_options"]["enable_resource_name_dns_aaaa_record"],
      "u_hostname_type": instance["private_dns_name_options"]["hostname_type"],
      "u_private_ip_address": instance["private_ip_address"],
      "u_public_dns_name": instance["public_dns_name"],
      "u_root_device_name": instance["root_device_name"],
      "u_root_device_type": instance["root_device_type"],
      "u_source_dest_check": instance["source_dest_check"],
      # "u_code": instance["code"],
      # "u_name": instance["name"],
      # "u_code": instance["code"],
      # "u_message": instance["message"],
      "u_state_transition_reason": instance["state_transition_reason"],
      "u_subnet": subnet_sys_id,
      "u_name": instance["tags"].get("Name", instance["instance_id"]),
      "u_aws_ec2launchtemplate_id": instance["tags"].get("aws:ec2launchtemplate:id", "N/A"),
      "u_aws_ec2launchtemplate_version": instance["tags"].get("aws:ec2launchtemplate:version", "N/A"),
      "u_usage_operation": instance["usage_operation"],
      "u_usage_operation_update_time": instance["usage_operation_update_time"],
      "u_virtualization_type": instance["virtualization_type"],
      "u_vpc": vpc_sys_id
    }