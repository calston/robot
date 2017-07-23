import copy
import exceptions
import json
import math
import time

import RPi.GPIO as gpio

from twisted.application import service
from twisted.internet import task, reactor, defer
from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.web import server, resource
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from . import web, robot

class DataProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.log.debug = lambda *a, **kw: None
        self.servos = robot.Servos()
        self.motor = robot.Motor()

        self.arm = [90, 50, 100, 90]
        self.arm_vector = [0, 0, 0, 0]

        self.t = task.LoopingCall(self.armTicker)

        self.t.start(0.01)

    def onMessage(self, payload, binary):
        if not binary:
            log.msg(payload)
            msg = json.loads(payload.decode('utf8'))
            cmd = msg['type']
            try:
                c = getattr(self, 'cmd_%s' % cmd.lower())
                return defer.maybeDeferred(c, msg['args'])
            except exceptions.AttributeError:
                log.msg("Command '%s' not implemented" % cmd)

    def armTicker(self):
        for i in range(4):
            if (self.arm_vector[i] == 1) and (self.arm[i] < 179):
                self.arm[i] += 1
                self.servos.rotateServo(i, self.arm[i])
            
            if (self.arm_vector[i] == -1) and (self.arm[i] > 1):
                self.arm[i] -= 1
                self.servos.rotateServo(i, self.arm[i])

    def cmd_arm_left(self, args):
        self.arm_vector[0] = 1
 
    def cmd_arm_right(self, args):
        self.arm_vector[0] = -1

    def cmd_arm_extend(self, args):
        self.arm_vector[1] = 1

    def cmd_arm_retract(self, args):
        self.arm_vector[1] = -1

    def cmd_arm_up(self, args):
        self.arm_vector[2] = 1

    def cmd_arm_down(self, args):
        self.arm_vector[2] = -1

    def cmd_arm_close(self, args):
        self.arm_vector[3] = 1

    def cmd_arm_open(self, args):
        self.arm_vector[3] = -1
        print self.arm

    def cmd_move_fwd(self, args):
        self.motor.forward()
        
    def cmd_move_back(self, args):
        self.motor.reverse()

    def cmd_move_left(self, args):
        self.motor.left()

    def cmd_move_right(self, args):
        self.motor.right()

    def cmd_stop(self, args):
        # Halt all movement
        self.motor.stop()
        self.arm_vector = [0, 0, 0, 0]

    def onClose(self, wasClean, code, reason):
        #self.cmd_stop_buffer_stream(None)
        pass

class RobotService(service.Service):

    def startService(self):
        root = resource.Resource()

        root.putChild('', web.Index(self))
        root.putChild("static", File(FilePath('robot/resources/static').path))

        site = server.Site(root)

        reactor.listenTCP(8081, site)

        factory = WebSocketServerFactory(u"ws://127.0.0.1:8082")
        factory.protocol = DataProtocol

        reactor.listenTCP(8082, factory)

    def stopService(self):
        gpio.cleanup()
