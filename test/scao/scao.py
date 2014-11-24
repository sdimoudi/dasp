#mpirun -np 1 -hostlist n1-c437  /usr/local/bin/mpipython $PWD/thisfile.py
#Python code created using the simulation setup GUI...
#Order of execution may not be quite optimal - you can always change by hand
#for large simulations - typically, the order of sends and gets may not be
#quite right.  Anyway, enjoy...
import numpy
import util.Ctrl
import base.mpiGet
import base.mpiSend
import base.shmGet
import base.shmSend
import Scientific.MPI
import science.infScrn
import science.infAtmos
import science.xinterp_dm
import science.wfscent
import science.tomoRecon
import science.science
ctrl=util.Ctrl.Ctrl(globals=globals())
print "Rank %d imported modules"%ctrl.rank
#Set up the science modules...
newMPIGetList=[]
newMPISendList=[]
newSHMGetList=[]
newSHMSendList=[]
infScrnList=[]
infAtmosList=[]
dmList=[]
wfscentList=[]
reconList=[]
scienceList=[]
ctrl.doInitialPokeThenRun()
#Add any personal code after this line and before the next, and it won't get overwritten
if ctrl.rank==0:
    infScrnList.append(science.infScrn.infScrn(None,ctrl.config,args={},idstr="L0"))
    infAtmosList.append(science.infAtmos.infAtmos({"L0":infScrnList[0],},ctrl.config,args={},idstr="a"))
    dmList.append(science.xinterp_dm.dm(None,ctrl.config,args={},idstr="dma"))
    wfscentList.append(science.wfscent.wfscent(dmList[0],ctrl.config,args={},idstr="a"))
    reconList.append(science.tomoRecon.recon({"a":wfscentList[0],},ctrl.config,args={},idstr="ngs"))
    scienceList.append(science.science.science(dmList[0],ctrl.config,args={},idstr="m"))
    dmList[0].newParent({"1":infAtmosList[0],"2":reconList[0],},"dma")
    execOrder=[infScrnList[0],infAtmosList[0],dmList[0],wfscentList[0],reconList[0],scienceList[0],]
    ctrl.mainloop(execOrder)
print "Simulation finished..."
#Add any personal code after this, and it will not get overwritten
Scientific.MPI.world.abort(0)

