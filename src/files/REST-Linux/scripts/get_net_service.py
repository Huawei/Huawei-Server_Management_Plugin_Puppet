# coding=utf-8

'''
#==========================================================================
# @Method: Query network service information commands.
# @command: getnetservice
# @Param: 
# @author: 
# @date: 2017.7.21
#==========================================================================
'''
import sys

HELP_INFO = '''specify service information(State and Port value).'''
PRINT_STYLE = "%-35s:     %s"


def getnetservice_init(parser, parser_list):
    '''
    #==========================================================================
    #   @Method:  Register and obtain network service information commands.
    #   @Param:   parser      major command argparser
                parser_list   save subcommand parser list
    #   @Return:  
    #   @author: 
    #   @date: 2017.7.22
    #==========================================================================
    '''

    sub_parser = parser.add_parser('getnetsvc', \
                                   help='''get network protocol information''')
    sub_parser.add_argument('-PRO', dest='Protocol',
                            choices=['HTTP', 'HTTPS', 'SNMP', 'VirtualMedia', 'IPMI', 'SSH', \
                                     'KVMIP', 'SSDP', 'VNC'],
                            required=False, help=HELP_INFO)
    parser_list['getnetsvc'] = sub_parser

    return 'getnetsvc'


def getnetservice(client, parser, args):
    '''
    #==========================================================================
    #   @Method:  Obtain network service information.
    #   @Param:   client   RedfishClient object
                parser   subcommand argparser. Export error messages when parameters are incorrect.
                args     parameter list
    #   @Return:  
    #   @author: 
    #   @date: 2017.7.22
    #==========================================================================
    '''
    # DTS2017082206482
    if parser is None and args is None:
        return None
    slotid = client.get_slotid()
    if slotid is None:
        return None
    url = "/redfish/v1/managers/%s/networkprotocol" % slotid
    resp = client.get_resource(url)
    if resp is None or resp.get("status_code", "") == "":
        return None

    if resp['status_code'] == 200:
        service_info = resp['resource']
        # Obtain the value of the Protocol attribute.
        key = args.Protocol
        flag = 0
        for oem_key in service_info:
            if oem_key == 'Oem':
                flag = 1
        if flag == 1:
            if service_info['Oem']['Huawei'] is None:
                parser.error('Failure: the -PRO parameter is invalid')
        if args.Protocol is not None:
            getspecifynetprop(service_info, key, parser)
            return resp
        getnetprop(service_info)

    elif resp['status_code'] == 404:
        print('Failure: resource was not found')
    return resp


def getspecifynetprop(service_info, key, parser):
    '''
    #==========================================================================
    #   @Method:  Obtain subfunctions of specified network service attributes.
    #   @Param:   service_info   Redfishsource object
                  key     specified parameter
    #   @Return:  
    #   @author: 
    #   @date: 2017.7.22
    #==========================================================================
    '''
    if service_info is None and key is None:
        sys.exit(127)

    # Specify the VNC to be queried and display information.
    if key == ('VNC'):
        # DTS2017081012468
        if service_info.get('Oem', '') == '' or \
                        service_info['Oem']['Huawei'][key] is None:
            parser.error('Failure: the -PRO parameter is invalid')
        print('')
        print('[%s]' % key)
        state = service_info['Oem']['Huawei'][key]['ProtocolEnabled']
        port = service_info['Oem']['Huawei'][key]['Port']
    # If the service is null or the enabling status is null, the service is not displayed. 
    # DTS2017081012468
    elif service_info.get(key, '') == '' or service_info[key] is None or \
                    service_info[key]['ProtocolEnabled'] is None:
        parser.error('Failure: the -PRO parameter is invalid')
    # Specify the non-OEM attribute to be queried and display information.
    else:
        print('')
        print('[%s]' % key)
        state = service_info[key]['ProtocolEnabled']
        port = service_info[key]['Port']
    print((PRINT_STYLE) % ("State", state))
    print((PRINT_STYLE) % ("Port", port))

    # Add other attributes in the SSDP protocol and display information.
    if key == ('SSDP'):
        notifyttl = service_info[key]['NotifyTTL']
        notifyipv6scope = service_info[key]['NotifyIPv6Scope']
        notifymulticastintervalseconds = service_info[key] \
            ['NotifyMulticastIntervalSeconds']
        print((PRINT_STYLE) % ("NotifyTTL", notifyttl))
        print((PRINT_STYLE) % ("NotifyIPv6Scope", notifyipv6scope))
        print((PRINT_STYLE) % ("NotifyMulticastIntervalSeconds", \
                               notifymulticastintervalseconds))

    return


def getnetprop(service_info):
    '''
    #==========================================================================
    #   @Method:  Obtain network service attribute subfunctions.
    #   @Param:   service_info   Redfishsource object
               
    #   @Return:  
    #   @author: 
    #   @date: 2017.7.22
    #==========================================================================
    '''
    if service_info is None:
        sys.exit(127)
    else:
        oem = None
        if 'Oem' in service_info:
            oem = service_info['Oem'].get('Huawei', None)

        for key in service_info:
            if key == ('@odata.context') or (key == '@odata.type') or \
                    (key == '@odata.id') or (key == 'Name') or (key == 'HostName') or \
                    (key == 'FQDN') or key == 'Id':
                continue

            # If the service is null, the service is not displayed.
            if not service_info.get(key, None):
                continue

            state = service_info[key].get('ProtocolEnabled', None)
            port = service_info[key].get('Port', None)
            # If the enabling status and the port are null, the service is not displayed.
            if (state is None) and (port is None):
                continue

            print('')
            print('[%s]' % key)
            print((PRINT_STYLE) % ("State", state))
            print((PRINT_STYLE) % ("Port", port))

            # Add other SSDP attributes and display information.
            if key == ('SSDP'):
                notifyttl = service_info[key]['NotifyTTL']
                notifyipv6scope = service_info[key]['NotifyIPv6Scope']
                notifymulticastintervalseconds = service_info[key] \
                    ['NotifyMulticastIntervalSeconds']
                print((PRINT_STYLE) % ("NotifyTTL", notifyttl))
                print((PRINT_STYLE) % ("NotifyIPv6Scope", notifyipv6scope))
                print((PRINT_STYLE) % ("NotifyMulticastIntervalSeconds", \
                                       notifymulticastintervalseconds))

            # if key == 'IPMI' and oem is not None and oem.get(key, None):
            #     for prop in oem.get(key):
            #         print((PRINT_STYLE) % (prop, oem.get(key).get(prop, None)))

        if oem is not None:
            getnetprop(oem)

    return
