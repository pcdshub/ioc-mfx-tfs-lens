# Makefile to install the st.cmd into the correctly location.
# Author: Jason Tiller

TOP = ../..
include $(TOP)/configure/CONFIG
ARCH = linux-x86_64
TARGETS = envPaths

# Make sure these archive files are fully expanded
USR_ARCHIVEFLAGS += -V

#----------------------------------------------------
# Create and install IOC archive file
#
ARCHIVE += ioc-mfx-tfs-lens.archive

#Create the IOC autosave file
REQ += ioc-mfx-tfs-lens.req

# See RULES.copy for more information on these variables.
COPY_ONLY_IF_NON_LOCAL=1
COPY_SUBDIR=iocBoot/ioc-tfs-mfx-lens
COPY_FILES=st.cmd

include $(CONFIG)/RULES
include $(CONFIG)/RULES.ioc-targets
