TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
#  Optimization of db files using dbst (DEFAULT: NO)
#DB_OPT = YES

#----------------------------------------------------
# Create and install (or just install)
# databases, templates, substitutions like this
DB_INSTALLS += $(IOCADMIN)/db/iocSoft.db
DB += lusiAtt4.db
DB += lusiAtt5.db
DB += lusiAtt6.db
DB += lusiAtt7.db
DB += lusiAtt8.db
DB += lusiAtt9.db
DB += lusiAtt10.db
DB += lusiAtt11.db
DB += lusiAtt12.db
DB += lusiFiltMotor.db
DB += lusiFiltPneumatic.db

#----------------------------------------------------
# Create and install (or just install)
# Archive files, templates, substitutions like this
#
ARCHIVE += lusiAtt-ioc.archive
ARCHIVE += lusiAtt.archive
ARCHIVE += lusiFilt.archive

#----------------------------------------------------
# Create and install (or just install)
# Autosave request files, templates, substitutions like this
#
REQ += lusiAtt-ioc.req
REQ += lusiAtt.req
REQ += lusiFilt.req

# Nothing to build for autosave, just install from $AUTOSAVE/db
DB_INSTALLS += $(AUTOSAVE)/db/save_restoreStatus.db

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

