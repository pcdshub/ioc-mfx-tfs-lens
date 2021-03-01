TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build an ioc application
# Use PROD_IOC_RTEMS for RTEMS only
# Use PROD_IOC_Linux for Linux only
PROD_IOC_Linux = lens

# lens.dbd will be created and installed
DBD += lens.dbd

# lens.dbd will be made up from these files:
lens_DBD += base.dbd
lens_DBD += iocAdmin.dbd
lens_DBD += autosaveSupport.dbd
lens_DBD += genSubRecord.dbd
lens_DBD += lensFocus.dbd
lens_DBD += lensLimit.dbd
lens_DBD += asyn.dbd
lens_DBD += modbus.dbd

# Install header for lookup tables
INC += lensTable.h
INC += interlockTables.h

# <name>_registerRecordDeviceDriver.cpp will be created from <name>.dbd
lens_SRCS += lens_registerRecordDeviceDriver.cpp
lens_SRCS_DEFAULT += lensMain.cpp

# Add locally compiled object code
lens_SRCS += lensFocus.c
lens_SRCS += limit.c
lens_SRCS += interlockTables.c

lens_LIBS += devIocStats
lens_LIBS += autosave
lens_LIBS += genSub
lens_LIBS += modbus
lens_LIBS += asyn
lens_LIBS += $(EPICS_BASE_IOC_LIBS)


#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

