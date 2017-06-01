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
#include <lensLimit.h>
/* 
    Look up a value from a pre-calculated table the low and/or high 
        INPUTS
            E = User input fundamental energy (eV)
            T = Type of limit evaluation, as defined in lensLimit.h

        OUTPUTS
            L = Lower limit of the acceptable operation range
            H = Higher limit of the acceptable operation range
*/
double find_limits(int l,int u, double E_list[], double L_list[],  double E)
{
    int m;
    double limit;
    while(l < u) {
        m = (l+u) /2;
        if( E==E_list[l] ) {
            u = l;
        }
        else if( E==E_list[m] ) {
            u = m;
            l = m;
        }
        else if( E == E_list[u] ){
            l = u;
        }
        else if( E < E_list[m] ) {
            if( u == m ) break;
                u = m;
        }
        else {
            if ( l == m ) break;
            l = m;
        }
    }
    double slope = 0.;
    if (u !=l) {
        slope = (L_list[u]-L_list[l])/(E_list[u]-E_list[l]);
    }
    limit  = L_list[l] + slope*(E-E_list[l]);
    return limit;

}


long limit_gensub_init(genSubRecord *pgsub)
{
    double E; /* Current beam energy*/
    E = *(double *)pgsub->e;
    return 0;
}

long limit_gensub_process(genSubRecord *pgsub)
{
    double E;   /*Current beam energy for first harmonic*/
    double L;   /*Low range of acceptable limit*/
    
    
    /*Check status of record*/
    if( pgsub == NULL)
        return -1;

    /*Retrieve current beam energy (eV)*/
    E = (*(double *)pgsub->e);
    char* T = (char*) pgsub->t;

    if(strcmp(T,MFX_ONLY)==0) {
        L = find_limits(0,126,E_MFX,MFX_LIMIT,E);
    }
    else if(strcmp(T,XRT_ONLY)==0) {
        L = find_limits(0,80,E_XRT,XRT_LIMIT,E);
    }
    else {
            L = 0.;
    }

    *(double *)pgsub->vall = L;

    pgsub->udf = FALSE;

    return 1;
}
epicsRegisterFunction(limit_gensub_init);
epicsRegisterFunction(limit_gensub_process);
