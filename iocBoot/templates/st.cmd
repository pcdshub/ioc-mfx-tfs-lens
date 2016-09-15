#!$$IOCTOP/bin/$$IF(ARCH,$$ARCH,linux-x86_64)/lens

< envPaths
epicsEnvSet( "IOCNAME",   "$$IOCNAME" )
epicsEnvSet( "ENGINEER",  "$$ENGINEER" )
epicsEnvSet( "LOCATION",  "$$LOCATION" )
epicsEnvSet( "IOCSH_PS1", "$(IOCNAME)> " )
epicsEnvSet( "IOC_PV",    "$$IOC_PV" )
epicsEnvSet( "IOCTOP",    "$$IOCTOP")
epicsEnvSet( "TOP",       "$$TOP")

cd( "$(IOCTOP)" )

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
drvAsynIPPortConfigure("lens-plc","$$PLC:502",0,0,1)

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
drvModbusAsynConfigure("BO_PORT",  "lens-plc", 0, 5,  0x8000, 256,   0,  100,  "BK")

# COIL Inputs (PLC -> EPICS) starting at 0x8000 on function code 2.
drvModbusAsynConfigure("BI_PORT",      "lens-plc", 0, 2,  0x8000, 256,    0,  100, "BK")


###################
#Assign Memory
####################
# Extra PLC memory output (EPICS -> PLC) starting at 0x3000 on function code 6 (0x0064 is 100 in hex).
# I set the modbus length to 100, that's how many 16-bit registers we are currently using, it can be longer
drvModbusAsynConfigure("aoFLOAT_PORT",  "lens-plc", 0, 6,  0x3000, 100,   7,  100,  "BK")

# FLOAT Inputs (PLC -> EPICS) starting at 0x3000 on function code 3, data type 7
drvModbusAsynConfigure("aiFLOAT_PORT",      "lens-plc", 0, 3,  0x3064, 100,    7,  100, "BK")

# DINT aka LONG Inputs (PLC -> EPICS) starting at 0x3500 on function code 3, data type 5
drvModbusAsynConfigure("aiLONG_PORT",      "lens-plc", 0, 3,  0x30C8, 100,    5,  100, "BK")

#####################
#Load Lenses
#####################
$$LOOP(LENS)
$$IF(PREV_LENS)

dbLoadRecords("db/lens.db", "LOCATION=$$LOCATION,LENSID=$$LENSID,RADIUS=$$RADIUS,Z=$$Z,Z_MOT=$$IF(Z_MOT,$$Z_MOT CPP,0),PREV_Z=$$PREV_LENS:IMAGE,PREV_CRL=$$PREV_LENS:LAST_CRL,Y_MOT=$$Y_MOT,IN_STATE=$$IN_STATE,PREV_MAG=$$PREV_LENS:IMAGE_MAG,SAFEBIT=$$IF(SAFEBIT,$$SAFEBIT,0.0),INBIT=$$IF(INBIT,$$INBIT,0.0)")

$$ELSE(PREV_LENS)

dbLoadRecords("db/lens.db", "LOCATION=$$LOCATION,LENSID=$$LENSID,RADIUS=$$RADIUS,Z=$$Z,Z_MOT=$$IF(Z_MOT,$$Z_MOT CPP,0),PREV_Z=$$LOCATION:LENS:BEAM:SOURCE,PREV_CRL=$$LOCATION:LENS:$$LENSID:Z,Y_MOT=$$Y_MOT,IN_STATE=$$IN_STATE,PREV_MAG=$$LOCATION:LENS:BEAM:SIZE,SAFEBIT=$$IF(SAFEBIT,$$SAFEBIT,0.0),INBIT=$$IF(INBIT,$$INBIT,0.0)")
$$ENDIF(PREV_LENS)
$$ENDLOOP(LENS)

#####################
#Load Beam Parameters
#####################
dbLoadRecords("db/beam.db","LOCATION=$$LOCATION,LAST_LENS=$$BEAMLAST_LENS0,BEAM_START=$$IF(BEAMSTART0,$$BEAMSTART0,0.0),BEAM_SIZE=$$IF(BEAMSIZE0,$$BEAMSIZE0 CPP,1),NLENS=$$COUNT(LENS)")

######################
#Load Limit Parameters
######################
$$LOOP(LIMIT)

dbLoadRecords("db/flexiblelimit.db","LOCATION=$$LOCATION,TYPE=$$CALC_TYPE,LIMIT=$$NAME,OFFSET=$$OFFSET")
$$ENDLOOP(LIMIT)


#####################
#Load Remaining Modbus PV
#####################
$$IF(LOCATION,MFX)
dbLoadRecords("db/mfx-modbus.db","LOCATION=$$LOCATION")
$$ENDIF(LOCATION)
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
