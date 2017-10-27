# -*- mode: python; python-indent: 4 -*-
import ncs
import _ncs
import socket
from ncs.application import Service
from ncs.dp import Action
import time


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        template = ncs.template.Template(service)
        template.apply('bgp-flowspec', vars)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    #@Service.post_modification
    #def cb_post_modification(self, tctx, op, kp, root, proplist):
#        with ncs.maapi.Maapi.start_trans_in_trans(tctx) as m:
#            auditlist = root.audit
#            auditentry = auditlist.create(time.time())
#              auditentry.user = tctx.username
#            auditentry.service_name = service.name

class AuditDiffIterator(object):
    def __init__(self):
        self.count = 0

    def __call__(self, kp, op, oldv, newv):
        self.log.info('kp={0}, op={1}, oldv={2}, newv={3}'.format(
            str(kp), str(op), str(oldv), str(newv)))
        self.count += 1
        return _confd.ITER_RECURSE

class AuditAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        self.log.info('action name: ', name)
        self.log.info('path: ', input.path)
        self.log.info('path: ', kp)
        self.log.info('transaction id: ', input.tid)
        self.log.info('user information: ', uinfo)
        self.log.info('user information: ', uinfo.actx_thandle)
        self.log.info('user information: ', uinfo.context)
#        with ncs.maapi.Maapi as m:
#            with ncs.maapi.Session(m, uinfo.username, uinfo.context) as s:
#                with m.attach(input.tid):



#        self.log.info('user information: ', _ncs.maapi.xpath2kpath(input.path))
#            with maapi.wctx.session(c, 'admin') as s : 
#                with maapi.wctx.trans(s, readWrite = _ncs.READ_WRITE) as t : 

#        socket_maapi = socket.socket()
#        with _ncs.maapi.connect(socket_maapi, ip=uinfo.addr, port=_ncs.NCS_PORT) connection:
#            with _ncs.maapi.
#            with _ncs.maapi.attach2(connection, uinfo.username, input.tid)
#        _ncs.maapi.diff_iterate(socket_maapi, input.tid, AuditDiffIterator, _ncs.ITER_WANT_P_CONTAINER)

        with ncs.maapi.single_write_trans(uinfo.username, uinfo.context) as t:
            service = ncs.maagic.get_node(t,path)
            self.log.info('Service Name: ', service.name)
            auditentry = service.audit.create(time.time())
            auditentry.user = tctx.username
            auditentry.service_name = service.name
            action_input = service.get_modifications.get_input()
            self.log.info('Service Name: ', service.name)
#            action_input.outformat = 'cli'
#            auditentry.configuration = service.get_modifications(action_input)
#            t.apply()

# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('bgpflowspec-servicepoint', ServiceCallbacks)
        self.register_action('bgpaudit-action', AuditAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
