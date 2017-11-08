
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.task import Task
from direct.showbase import *
import random
import sys
import math
import OSC

# A slightly fancier version that will let you set configure multiple devices a little nicer 



class Client:
    def __init__ (self, id, ip):
        self.id = id
        self.ip = ip
        self.client_obj = OSC.OSCClient()
        self.client_obj.connect((ip, 6666))
    def send (self, msg):
        self.client_obj.send(msg)
        
class Tracker_Obj:
    # get data from VRPN and apply it to a node in the scenegraph

    def __init__ (self, id):
        self.id = id 
        self.tracker = TrackerNode(g_VRPNClient,id)
        self.trackedNode = render.attachNewNode('trackedNode_' + id)  
        base.dataRoot.node().addChild(self.tracker)
        self.transform2node = Transform2SG('t2n_' + id)
        self.tracker.addChild(self.transform2node)      
        self.transform2node.setNode(self.trackedNode.node())
        
    def getPos (self):
        return self.trackedNode.getPos()
        
    def getHpr (self):
        return self.trackedNode.getHpr()
       
class World(DirectObject.DirectObject):
    def __init__(self):
    # Accept the Esc key to quit the game.
        self.accept("escape", sys.exit)

        self.tracker_objs = []
        self.tracker_objs.append(Tracker_Obj('Visor'))
        self.tracker_objs.append(Tracker_Obj('Wand'))

        taskMgr.add (self.update,"update")

        camera.lookAt(0,0,0)

        self.display1 = aspect2d.attachNewNode(TextNode('display1'))
        self.display1.node().setText("0 0 0")
        self.display1.setScale(0.1)
        self.display1.setPos(-1,0,0)
        
        '''
        # GUI Setup
          #add some text
        bk_text = "This is my Demo"
        textObject = OnscreenText(text = bk_text, pos = (-1.0,0.95), 
        scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1)    
        #callback function to set  text 
        def setText(textEntered):
            textObject.setText(textEntered)
         
        #clear the text
        def clearText():
            b.enterText('')        
        # Broadcast IP
        DirectLabel (text = "Send Data to IP Address:", pos=(.1,0,-.1),scale=.05,parent=base.a2dTopLeft,text_align=TextNode.ALeft,text_fg=(1,1,1,1),text_bg=(0,0,0,1))
        b = DirectEntry(text = "" , parent=base.a2dTopLeft,scale=.05, pos = (.8,0,-.1), command=setText,initialText="Type Something", numLines = 1,focus=1,focusInCommand=clearText)
        '''
        
    def update (self,t):
        g_VRPNClient.poll()
        
        vp = self.tracker_objs[0].getPos()
        vr = self.tracker_objs[0].getHpr()
                
        msg = OSC.OSCMessage()
        msg.setAddress("/visor")
        msg.append(vp.getX())
        msg.append(vp.getY())
        msg.append(vp.getZ())
        msg.append(vr.getX())
        msg.append(vr.getY())
        msg.append(vr.getZ())
        
        for client in g_clients:
            client.send(msg)

        wp = self.tracker_objs[1].getPos()
        wr = self.tracker_objs[1].getHpr()
        
        msg = OSC.OSCMessage()
        msg.setAddress("/wand")
        msg.append(wp.getX())
        msg.append(wp.getY())
        msg.append(wp.getZ())
        msg.append(wr.getX())
        msg.append(wr.getY())
        msg.append(wr.getZ())
        
        for client in g_clients:
            client.send(msg)
            
           
        #msg.append("%f %f %f %f %f %f"%(vp.getX() , vp.getY() , vp.getZ( ) , vr.getX(), vr.getY(), vr.getZ()))
        #print (vp.getX(), vp.getY(), vp.getZ())
        #self.display1.node().setText("visor:\n%0.3f\n%0.3f\n%0.3f\nred hat:\n%0.3f\n%0.3f\n%0.3f" % (vp.getX(), vp.getY(), vp.getZ(), rp.getX(), rp.getY(), rp.getZ()))
        
        
        #client.send(msg)
         

        
        #msg = OSC.OSCMessage()
        #msg.setAddress("/wand")
        
        # offsets for wand position
        #msg.append("%f %f %f %f %f %f"%(wp.getX() , wp.getY() , wp.getZ(),wr.getX(), wr.getY(), wr.getZ() ))
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
        
        #for client in g_clients:
         #   client.send(msg)

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
        

g_clients = []
g_clients.append(Client('Riker', '129.161.12.207'))
g_VRPNClient = VrpnClient ('localhost')
w=World()
run()
