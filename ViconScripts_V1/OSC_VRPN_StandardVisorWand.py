
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.showbase import *
import random
import sys
import math
import OSC

class Client:
    def __init__ (self, id, ip):
        self.id = id
        self.ip = ip
        self.client_obj = OSC.OSCClient()
        self.client_obj.connect((ip, 6666))
    def send (self, msg):
        self.client_obj.send(msg)
        
class Tracker_Obj:
    def __init__ (self, vrpnclient, id):
        self.id = id 
        self.tracker = TrackerNode(vrpnclient,id)
       
clients = []
clients.append(Client('Riker', '129.161.12.207'))


class World(DirectObject.DirectObject):
    def __init__(self):
    # Accept the Esc key to quit the game.
        self.accept("escape", sys.exit)

        self.vrpnclient = VrpnClient ('localhost')
        
        tracker_objs = []
        tracker_objs.append(Tracker_Obj(self.vrpnclient, 'Visor'))
        tracker_objs.append(Tracker_Obj(self.vrpnclient, 'Wand'))
        
        self.tracker0 = TrackerNode(self.vrpnclient,"Visor")
        self.tracker1 = TrackerNode(self.vrpnclient,"Wand")
        #self.tracker2 = TrackerNode(self.vrpnclient, "redhat")
        
        #we're trying to add the staff to be recognized, srry if code breaks :'(
        #self.tracker3 = TrackerNode(self.vrpnclient,"Staff")
        
        taskMgr.add (self.update,"update")

        self.trackedVisorNode = render.attachNewNode('trackedVisorNode')  
        base.dataRoot.node().addChild(self.tracker0)
        
        self.trackedWandNode = render.attachNewNode('trackedWandNode')  
        base.dataRoot.node().addChild(self.tracker1) 
        
        #I just copied the thing above but changed stuff to staff
        #self.trackedStaffNode = render.attachNewNode('trackedstaffNode')  
        #base.dataRoot.node().addChild(self.tracker3) 
        
        #self.trackedRedHatNode = render.attachNewNode('trackedRedHatNode')  
        #base.dataRoot.node().addChild(self.tracker2) 
       
        t2nVisor = Transform2SG('t2nVisor')
        self.tracker0.addChild(t2nVisor)      
        t2nVisor.setNode(self.trackedVisorNode.node())
        
        t2nWand = Transform2SG('t2nWand')
        self.tracker1.addChild(t2nWand)      
        t2nWand.setNode(self.trackedWandNode.node())
        
        #also copying the stuff above for the staff
        #t2nStaff = Transform2SG('t2nStaff')
        #self.tracker1.addChild(t2nStaff)      
        #t2nStaff.setNode(self.trackedStaffNode.node())
        
        #t2nRedHat = Transform2SG('t2nRedHat')
        #self.tracker2.addChild(t2nRedHat)      
        #t2nRedHat.setNode(self.trackedRedHatNode.node())

        camera.lookAt(0,0,0)

        self.display1 = aspect2d.attachNewNode(TextNode('display1'))
        self.display1.node().setText("0 0 0")
        self.display1.setScale(0.1)
        self.display1.setPos(-1,0,0)
        
        #initialize kalman filters
        #krx = KalmanFilter()
        #kry = KalmanFilter()
        #krz = KalmanFilter()
        
        
    def update (self,t):
        self.vrpnclient.poll()
       
        vp = self.trackedVisorNode.getPos()
        vr = self.trackedVisorNode.getHpr()
        
        #rp = self.trackedRedHatNode.getPos()
        
        msg = OSC.OSCMessage()
        msg.setAddress("/visor")
        msg.append("%f %f %f %f %f %f"%(vp.getX() , vp.getY() , vp.getZ( ) , vr.getX(), vr.getY(), vr.getZ()))
        #print (vp.getX(), vp.getY(), vp.getZ())
        #self.display1.node().setText("visor:\n%0.3f\n%0.3f\n%0.3f\nred hat:\n%0.3f\n%0.3f\n%0.3f" % (vp.getX(), vp.getY(), vp.getZ(), rp.getX(), rp.getY(), rp.getZ()))
        
        
        #client.send(msg)
         
        wp = self.trackedWandNode.getPos()
        wr = self.trackedWandNode.getHpr()
        
        #msg = OSC.OSCMessage()
        #msg.setAddress("/wand")
        
        # offsets for wand position
        msg.append("%f %f %f %f %f %f"%(wp.getX() , wp.getY() , wp.getZ(),wr.getX(), wr.getY(), wr.getZ() ))
        #msg.append("%f %f %f %f %f %f"%(wp.getX() , wp.getY(), wp.getZ(), krx.filter( wr.getX() ), kry.filter( wr.getY() ), krz.filter( wr.getZ() ) ))
        
        #msg.setAddress("/redhat")
        #rhp = self.trackedRedHatNode.getPos()
        #rhr = self.trackedRed
        #HatNode.getHpr()
        #msg.ap pend("%f %f %f %f %f %f"%(rhp.getX(), rhp.getY(), rhp.getZ(), rhr.getX(), rhr.getY(), rhr.getZ()))
        
        #and now for the staff messenge appending thing
        #sp = self.trackedStaffNode.getPos()
        #sr = self.trackedStaffNode.getHpr()
        
        #msg.append("%f %f %f %f %f %f"%(sp.getX() , sp.getY() , sp.getZ(),sr.getX(), sr.getY(), sr.getZ() ))
        
        for client in clients:
            client.send(msg)

       # print vp, vr, wp, wr

        self.display1.node().setText("visor:\n%0.3f\n%0.3f\n%0.3f\nwand:\n%0.3f\n%0.3f\n%0.3f  " % (vp.getX(), vp.getY(), vp.getZ(), wp.getX(), wp.getY(), wp.getZ()))

               
        return Task.cont
        
""" 
class KalmanFilter(object):
    #filter(z) -> x at this timestep
    #-----------------------------------------------------
    #KALMAN FILTER
    #-----------------------------------------------------
    #x sub(k) = A x sub(k - 1) + B u sub(k) + w sub(k - 1)
    #TRANSLATION: (current x = previous x + some control input + some noise)
    #Z sub(k) = H x sub(k) + v sub(k)

    #TRANSLATION: measured values are (signal value + measurement noise)
    def __init__(self):
        #Global vars: I am a bad person ....
        #Set up values
        self.k = 1      #initial value. This is the iterator. ( think t in f(t) )
        self.prev_x = 0 #initial value
        self.x = 0      #state?
        self.prev_p = 1 #initial value
        self.p = 0      #error covariance?
        self.a = 1      #some coefficient
        self.b = 1      #some coefficient
        self.h = 1      #some coefficient
        self.t = 1      #some power
        self.r = 0.1    #% amount of noise, roughly?
        self.u = 0      #?
        self.q = 0      #?
        self.z = 0.5    #Z is your input. (z sub(k) = H sub(k) + v sub(k)) (measured vals are signal + noise)
        self.g = 0      #G is the kalman gain

    def predict():
        #project the state ahead
        self.x = self.a * self.prev_x + self.b * self.u #u sub(k) is 0?
        #project the error covaraince
        self.p = self.a * self.prev_p * self.a ** self.t + self.q

    def correct():
 
        #compute the kalman gain (g)... I use g instead of K sub (k) b/c K vs k is confusing
        self.g = self.prev_p * self.h ** self.t / (self.h * self.prev_p * self.h ** self.t + self.r)
        #update the estimate via z
        self.x = self.prev_x + self.g * (self.z - self.h * self.prev_x)
        #update the error covariance
        self.p = (1 - self.g * self.h) * self.prev_p
        #print
        #print( "x = " + str(self.x) + ", p = " + str(self.p) )
        #print( "z = " + str(self.z) )

    def main():
        #TODO: Get the measured value, or Z
     
        self.predict()
        self.correct()
        #update indecies
        self.k = self.k + 1
        self.prev_x = self.x
        self.prev_p = self.p
        
    def filter( input ):
        self.z = input
        self.main()
        return self.x
        """
        

w=World()
run()
