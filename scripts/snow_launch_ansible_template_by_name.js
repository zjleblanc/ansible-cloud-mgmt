try { 
  var req_template_id = new sn_ws.RESTMessageV2('Ansible Automation Platform', 'Get Template Id');
  req_template_id.setStringParameterNoEscape('template_type', current.variables.template_type);
  req_template_id.setStringParameterNoEscape('template_name', current.variables.template_name);

  var resp_template_id = req_template_id.execute();
  var resp_template_id_json = JSON.parse(resp_template_id.getBody());

  if(resp_template_id_json["count"] <= 0) {
    throw new Error("No " + current.variables.template_type + " template found with name " + current.variables.template_name);
  }

  var r_launch_template = new sn_ws.RESTMessageV2('Ansible Automation Platform', 'Launch Ansible Template');
  r_launch_template.setStringParameterNoEscape('decomm_cat_item', current.cat_item);
  r_launch_template.setStringParameterNoEscape('decomm_ritm', current.number);
  r_launch_template.setStringParameterNoEscape('decomm_sys_id', current.sys_id);
  r_launch_template.setStringParameterNoEscape('decomm_requested_for', current.requested_for);
  r_launch_template.setStringParameterNoEscape('template_id', resp_template_id_json["results"][0]["id"].toString());
  
  var resp_launch_template = r_launch_template.execute();
}
catch(ex) {
  var message = ex.message;
}