#!$$IOCTOP/bin/$$IF(ARCH,$$ARCH,linux-x86_64)/lens

< envPaths
epicsEnvSet( "IOCNAME", "$$IOCNAME" )
epicsEnvSet( "ENGINEER", "$$ENGINEER" )
epicsEnvSet( "LOCATION", "$$LOCATION" )
epicsEnvSet( "IOCSH_PS1", "$(IOCNAME)> " )
epicsEnvSet( "IOC_PV", "$$IOC_PV" )
epicsEnvSet("IOCTOP", "$$IOCTOP")
epicsEnvSet("TOP", "$$TOP")

cd( "$(IOCTOP)" )

# Run common startup commands for linux soft IOC's
< /reg/d/iocCommon/All/pre_linux.cmd

# Register all support components
dbLoadDatabase("dbd/lens.dbd")
lens_registerRecordDeviceDriver(pdbbase)

# Load Lens IOC

$$LOOP(LENS)
$$IF($$INDEX,0)
dbLoadRecords("db/lens.db", "LOCATION=$$LOCATION,LENSID=$$ID,NLENS=$$NLENS,RADIUS=$$RADIUS,Z=$$IF($$Z,$$Z,0),Z_MOT=$$IF($$Z_MOT,$$Z,0),OBJECT=0.0)
$$ELSE($$INDEX)
dbLoadRecords("db/lens.db", "LOCATION=$$LOCATION,LENSID=$$ID,NLENS=$$NLENS,RADIUS=$$RADIUS,Z=$$IF($$Z,$$Z,0),Z_MOT=$$IF($$Z_MOT,$$Z,0),OBJECT=$$LOCATION:LENS:$$LENSID$$CALC{$$INDEX-1}:FOCUS")
$$ENDIF($$INDEX)
$$IF($$INDEX,$$CALC{$$COUNT(LENS)-1}
dbLoadRecords("db/lens.db", "LOCATION=$$LOCATION,LENSID=$$ID,NLENS=$$NLENS,RADIUS=$$RADIUS,Z=$$IF($$Z,$$Z,0),Z_MOT=$$IF($$Z_MOT,$$Z,0),OBJECT=$$LOCATION:LENS:$$LENSID$$CALC{$$INDEX-1}:FOCUS")
dbLoadRecords("db/beam.db", "LOCATION=$$LOCATION,HIGH_LIMIT=$$HIGH_LIMIT,LOW_LIMIT=$$LOW_LIMIT,FOCUS=$$LOCATION:LENS:$$LENSID:FOCUS")
$$ENDIF($$INDEX)
$$IF($$Y_MOT)
dbLoadRecords("db/stacklens1.db", "LOCATION=$$LOCATION,MOTID=$$ID,LENSID=$$ID,Y_MOT=$$Y_MOT,IN_STATE=$$IF($$IN_STATE,$$IN_STATE,IN)")
$$ENDIF($$Y_MOT)
$$ENDLOOP(LENS)

$$LOOP(STACK)
$$IF($$NLENS,3)
dbLoadRecords("dbstacklens3.db", "LOCATION=$$LOCATION,MOTID=$$ID,Y_MOT=$$Y_MOT,LENS1_ID=$$LENS1_ID,LENS1_STATE=$$LENS1_STATE,LENS2_ID=$$LENS2_ID,LENS2_STATE=$$LENS2_STATE,LENS3_ID=$$LENS3_ID,LENS3_STATE=$$LENS3_STATE)
$$ENDIF($$NLENS)
$$ENDLOOP(STACK)
# Load default record instances
dbLoadRecords( "db/iocSoft.db",             "IOC=$(IOC_PV)" )
dbLoadRecords( "db/save_restoreStatus.db",  "IOC=$(IOC_PV)" )

# Setup autosave
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
