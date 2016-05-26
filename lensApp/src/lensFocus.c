#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <complex.h>

#include <dbEvent.h>
#include <dbDefs.h>
#include <dbCommon.h>
#include <registryFunction.h>
#include <epicsExport.h>
#include <recSup.h>
#include <genSubRecord.h>
#include <lensTable.h>
/* 
    Do a calculation to determine the Focus of a set of Beryllium Lens based
    on the photon Energy of a incoming Xray beam.

        INPUTS
            E = user input fundamental energy (eV)
            N = Number of Lenses in the set
            R = Effective radius of curvature (m)

        OUTPUTS
            F = Focus of the lens at the specified energy
*/

/* Energy range struct */
typedef struct {
  int l;
  int u;
} Range;

Range search_energy(int l,int u, double E)
{
    int m;
    while(l < u) {
        m = (l+u) /2;
        if( E==Etab[l] ) {
            u = l;
        }
        else if( E==Etab[m] ) {
            u = m;
            l = m;
        }
        else if( E == Etab[u] ){
            l = u;
        }
        else if( E < Etab[m] ) {
            if( u == m ) break;
            u = m;
        } else {
           if ( l == m ) break;
          l = m;
        }
    }
    return (Range) {l,u}; 
}

/*Effective radius of each lens (m) */
static double Rad = 0;

long lensFocus_gensub_init(genSubRecord *pgsub)
{
    Rad = *(double *)pgsub->r;
    return 0;
}

long lensFocus_gensub_process(genSubRecord *pgsub)
{
    double E;          /*Current beam energy for first harmonic*/
    double R;          /*Effective Radius of Lens*/
    long N;            /*Number of Lenses*/
    double f1,f2;      /*The real and imaginary values of
                        *the index of refraction*/
    double complex f0; /*The complex index of refraction*/
    double complex f;  /*Be index of refraction*/
    double delta;      /*Delta value*/
    double lambda;     /*Wavelength of Beam in meters*/ 
    double focus;      /*focus*/
    /*Check status of record*/
    if( pgsub == NULL)
        return -1;

    /*Retrieve current beam energy (eV)*/
    E = (*(double *)pgsub->e);
    N = (*(long *)pgsub->n);
    R = (*(double *)pgsub->r);
    /*If current energy is lower than table*/
    if (E<Etab[0] )
    {
        f1 = F1tab[0];
        f2 = F2tab[0];
    }
    else if (E > Etab[HIGH_FUND])
    {
        f1 = F1tab[HIGH_FUND];
        f2 = F2tab[HIGH_FUND];
    }
    /*Else, interpolate value*/
    else
    {
        Range r;
        double slope_f1 = 0., slope_f2 = 0.;
        r = search_energy(0,HIGH_FUND,E);
        if (r.u !=r.l) {
            slope_f1 = (F1tab[r.u]-F1tab[r.l])/(Etab[r.u]-Etab[r.l]);
            slope_f2 = (F2tab[r.u]-F2tab[r.l])/(Etab[r.u]-Etab[r.l]);
        }
        f1 = F1tab[r.l] + slope_f1*(E-Etab[r.l]);
        f2 = F2tab[r.l] + slope_f2*(E-Etab[r.l]);
    }

    /*Calculate index of refraction*/
    f0 = f1+f2*I;

    /*Calculate lens characteristic*/
    f = f0*p_be*NA/m_be; 

    /*Calculate delta*/
    lambda = (12389.4/E)*1E-10;
    delta  = creal(eRad*pow(lambda,2.)*f/(2*pi));

    /*Calculate focus*/
    focus = R/(2*N*delta)*(1-N*delta);

    /*Push values out*/
    *(double *)pgsub->valf = focus;

    pgsub->udf = FALSE;
}

epicsRegisterFunction(lensFocus_gensub_init);
epicsRegisterFunction(lensFocus_gensub_process);
