# A description of what this class does
#
# @summary Get RAID Health
#
# @example
#   ../../../examples/raid_health_get.pp
#
define rest::system::raid::health (
  $ibmc_username  = 'username',
  $ibmc_password  = 'password',
  $ibmc_host      = '127.0.0.1',
  $ibmc_port      = '443',
) {

  # init rest
  include ::rest

  $script = "sh rest -H '${ibmc_host}' -p ${ibmc_port} -U '${ibmc_username}' -P '${ibmc_password}' --error-code"
  $command = 'getraidhealth'

  exec { $title:
    command => Sensitive.new("${script} ${command}"),
    *       => $rest::service::context,
  }

}
