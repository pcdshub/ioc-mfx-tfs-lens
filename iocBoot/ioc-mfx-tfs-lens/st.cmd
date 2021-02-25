#!../../bin/linux-x86_64/lens

< envPaths
epicsEnvSet( "IOCNAME",   "ioc-mfx-tfs-lens" )
epicsEnvSet( "ENGINEER",  "Teddy Rendahl (trendahl)" )
epicsEnvSet( "LOCATION",  "MFX" )
epicsEnvSet( "IOCSH_PS1", "$(IOCNAME)> " )
epicsEnvSet( "IOC_PV",    "IOC:MFX:LENS" )

cd( "../.." )

# Run common startup commands for linux soft IOC's
< /reg/d/iocCommon/All/pre_linux.cmd

# Register all support components
dbLoadDatabase("dbd/lens.dbd")
lens_registerRecordDeviceDriver(pdbbase)

######################################################################################
# Beckhoff ModBus TCP Client Setup
# Here we set up the various ports for the Beckhoff PLC modbus interface
######################################################################################

# Use the following commands for TCP/IP
#drvAsynIPPortConfigure(const char *portName, 
#                       const char *hostInfo,
#                       unsigned int priority, 
#                       int noAutoConnect,
#                       int noProcessEos);
drvAsynIPPortConfigure("lens-plc","172.21.72.99:502",0,0,1)

#modbusInterposeConfig(const char *portName, 
#                      int slaveAddress, 
#                      modbusLinkType linkType,
#                      int timeoutMsec)
modbusInterposeConfig("lens-plc",0,0,0)

# Make sure that these port configurations include the correct modbusLength,
# otherwise you might see your records initialize as unconnected...

#drvModbusAsynConfigure(portName, 
#                       tcpPortName,
#                       slaveAddress, 
#                       modbusFunction, 
#                       modbusStartAddress, 
#                       modbusLength,
#                       dataType,  #0-UINT16, 7-FLOAT32LE, 8-FLOAT32BE
#                       pollMsec, 
#                       plcType);


####################
#Assign Coils
####################
# COIL Outputs (EPICS -> PLC) starting at 0x8000 on function code 5.
drvModbusAsynConfigure("BO_PORT",  "lens-plc", 0, 5,  0x8000, 256,   0,  50, "BK")

# COIL Inputs (PLC -> EPICS) starting at 0x8000 on function code 2.
drvModbusAsynConfigure("BI_PORT",      "lens-plc", 0, 2,  0x8000, 256,    0,  50, "BK")


###################
#Assign Memory
####################
# Extra PLC memory output (EPICS -> PLC) starting at 0x3000 on function code 6 (0x0064 is 100 in hex).
# I set the modbus length to 100, that's how many 16-bit registers we are currently using, it can be longer
drvModbusAsynConfigure("aoFLOAT_PORT",  "lens-plc", 0, 6,  0x3000, 100,   7,  50,  "BK")

# FLOAT Inputs (PLC -> EPICS) starting at 0x3000 on function code 3, data type 7
drvModbusAsynConfigure("aiFLOAT_PORT",      "lens-plc", 0, 3,  0x3064, 125,    7,  50, "BK")

# DINT aka LONG Inputs (PLC -> EPICS) starting at 0x3500 on function code 3, data type 5
drvModbusAsynConfigure("aiLONG_PORT",      "lens-plc", 0, 3,  0x30C8, 100,    5,  50, "BK")

#####################
#Load Lenses
#####################
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:01,Y_MOT=MFX:TFS:XFLS:01,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:02,Y_MOT=MFX:TFS:XFLS:02,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:03,Y_MOT=MFX:TFS:XFLS:03,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:04,Y_MOT=MFX:TFS:XFLS:04,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:05,Y_MOT=MFX:TFS:XFLS:05,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:06,Y_MOT=MFX:TFS:XFLS:06,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:07,Y_MOT=MFX:TFS:XFLS:07,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:08,Y_MOT=MFX:TFS:XFLS:08,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:09,Y_MOT=MFX:TFS:XFLS:09,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=TFS:10,Y_MOT=MFX:TFS:XFLS:10,Z_MOT=MFX:TFS:MMS:21.RBV,IN_STATE=IN")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=DIA:01,Y_MOT=MFX:DIA:XFLS,Z_MOT=,IN_STATE=6K70")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=DIA:02,Y_MOT=MFX:DIA:XFLS,Z_MOT=,IN_STATE=7K50")
dbLoadRecords("db/lens.db", "LOCATION=$(LOCATION),LENSID=DIA:03,Y_MOT=MFX:DIA:XFLS,Z_MOT=,IN_STATE=9K45")

#####################
#Load Beam Parameters
#####################
dbLoadRecords("db/beam.db", "LOCATION=$(LOCATION), NLENS=13, ENERGY=SIOC:SYS0:ML00:AO627") 

######################
#Load Limit Parameters
######################
dbLoadRecords("db/flexiblelimit.db","LOCATION=$(LOCATION),TABLE_NAME=TABLE_NO_LENS,LIMIT=NO_LENS")
dbLoadRecords("db/flexiblelimit.db","LOCATION=$(LOCATION),TABLE_NAME=TABLE_LENS1_750,LIMIT=LENS1")
dbLoadRecords("db/flexiblelimit.db","LOCATION=$(LOCATION),TABLE_NAME=TABLE_LENS2_428,LIMIT=LENS2")
dbLoadRecords("db/flexiblelimit.db","LOCATION=$(LOCATION),TABLE_NAME=TABLE_LENS3_333,LIMIT=LENS3")
dbLoadRecords("db/monitor.db", "LOCATION=$(LOCATION)")


#####################
#Load Remaining Modbus PV
#####################
dbLoadRecords("db/mfx-modbus.db","LOCATION=$(LOCATION)")

###################
#Load Shutter PVs #
###################
dbLoadRecords("db/shutter.db", "LOCATION=$(LOCATION), SHUTTER=MFX:ATT:11")

###############################
# Load default record instances
###############################
dbLoadRecords( "db/iocSoft.db",             "IOC=$(IOC_PV)" )
dbLoadRecords( "db/save_restoreStatus.db",  "IOC=$(IOC_PV)" )


###############################
# Setup autosave
###############################
set_savefile_path( "$(IOC_DATA)/$(IOCNAME)/autosave" )
set_requestfile_path( "$(TOP)/autosave" )
save_restoreSet_status_prefix( "$(IOC_PV):" )
save_restoreSet_IncompleteSetsOk( 1 )
save_restoreSet_DatedBackupFiles( 1 )
set_pass0_restoreFile( "$(IOCNAME).sav" )
set_pass1_restoreFile( "$(IOCNAME).sav" )

# Initialize the IOC and start processing records
iocInit()

# Start autosave backups
create_monitor_set( "$(IOCNAME).req", 5, "IOC=$(IOC_PV)" )

# All IOCs should dump some common info after initial startup.
< /reg/d/iocCommon/All/post_linux.cmd
