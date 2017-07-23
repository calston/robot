from zope.interface import implements
 
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
 
import robot
 
class Options(usage.Options):
    optParameters = [
    ]
 
class RobotServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "robot"
    description = "robot"
    options = Options
 
    def makeService(self, options):
        return robot.makeService()
 
serviceMaker = RobotServiceMaker()
