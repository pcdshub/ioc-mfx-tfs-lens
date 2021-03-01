#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

#include <dbEvent.h>
#include <dbDefs.h>
#include <dbCommon.h>
#include <registryFunction.h>
#include <epicsExport.h>
#include <recSup.h>
#include <genSubRecord.h>

#include "interlockTables.h"

const RangeTable *tables[] = {
    &TABLE_NO_LENS, &TABLE_LENS3_333, &TABLE_LENS2_428, &TABLE_LENS1_750
};
const int N_TABLES = 4;

long limit_gensub_init(genSubRecord *pgsub)
{
    double E; /* Current beam energy*/
    E = *(double *)pgsub->e;
    return 0;
}

long limit_gensub_process(genSubRecord *pgsub)
{
    double energy;             /*Current beam energy for first harmonic*/
    double range_low = 0.0;    /*Low range of trip region*/
    double range_high = 0.0;   /*High range of trip region*/

    /*Check status of record*/
    if( pgsub == NULL)
        return -1;

    /*Retrieve current beam energy (eV)*/
    energy = (*(double *)pgsub->e);

    int table_idx;
    const char* table_name = (const char*) pgsub->t;
    RangeRow row;

	for (table_idx=0; table_idx < N_TABLES; table_idx++) {
        if (!strcmp(tables[table_idx]->table_name, table_name)) {
            if (find_limits(&row, tables[table_idx], energy)) {
                range_low = row.low;
                range_high = row.high;
            }
            break;
		}
	}


    *(double *)pgsub->vall = range_low;
    *(double *)pgsub->valh = range_high;

    pgsub->udf = FALSE;

    return 1;
}
epicsRegisterFunction(limit_gensub_init);
epicsRegisterFunction(limit_gensub_process);
