# A description of what this class does
#
# @summary Delete License
# @example ../../examples/license_delete.pp
#
define rest::bmc::license::delete (
  String $ibmc_username    = 'username',
  String $ibmc_password    = 'password',
  String $ibmc_host        = '127.0.0.1',
  String $ibmc_port        = '443',
) {


  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = "deletelicense"

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }
}
