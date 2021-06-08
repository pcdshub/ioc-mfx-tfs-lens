ioc-mfx-tfs-lens
================

MFX transfocator lens IOC.

**Warning**
-----------

This IOC code is used to interface EPICS PVs with the PLC
``lcls-plc-mfx-be-lens-interlock``.

* This PLC code is part of a safety interlock. The LCLS Safety Office needs to be
  contacted prior to loading any changes on the PLC.
* ``ioc-mfx-tfs-lens``, as the corresponding EPICS IOC code, requires that the
  LCLS Safety Office be contacted prior to pushing any changes to production.
* Attenuator 11 of ``ioc-mfx-lusiAtt`` shall not be disabled, as it is an
  integral part of this safety interlock: it is being used as a beam shutter.

Interlock system
----------------

Part of the Beryllium lens interlock system, paired with
[pcdshub/lcls-plc-mfx-be-lens-interlock](https://github.com/pcdshub/lcls-plc-mfx-be-lens-interlock)

![Disallowed region plot](./interlock_regions.png)

Additional criteria:

| Pre-focus | Minimum energy [keV] | Requires transfocator lens low [keV] | Requires transfocator lens high [keV] |
|-----------|----------------------|--------------------------------------|---------------------------------------|
| NO_LENS   | 0                    | n/a                                  | n/a                                   |
| LENS3_333 | 9.5                  | 9.5                                  | 11.11                                 |
| LENS2_428 | 8.28                 | 8.28                                 | 10.02                                 |
| LENS1_750 | 5.96                 | 5.96                                 | 8.02                                  |

1. Regardless of transfocator setting, the minimum energy must be greater than or
   equal to that shown in the table (Minimum energy [keV]).  Trip if below.

2. When a pre-focusing lens is inserted, there exists a range of photon
   energies in which at least one transfocator lens must be inserted.
   If the current photon energy is within this (inclusive) range and no
   lens is inserted, trip.

Related repositories
--------------------

Automated calculation of beryllium lens focusing optics for MFX Transfocator with ophyd in Python:
* [transfocate](https://github.com/pcdshub/transfocate)
* [lcls-plc-mfx-be-lens-interlock](https://github.com/pcdshub/lcls-plc-mfx-be-lens-interlock)
