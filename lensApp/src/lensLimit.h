#ifndef _INCLUDE_LIMIT_H
#define _INCLUDE_LIMIT_H


/*Define Constants used for Calculations*/
#define MFX_ONLY     "mfx_only"
#define XRT_ONLY     "xrt_only" 
#define PREFOCUS_MFX "prefocus_mfx"


static double Etab[100] = 
{    
    400.0, 525.25, 650.51, 775.76, 901.01,
    1026.3, 1151.5, 1276.8, 1402.0, 1527.3,
    1652.5, 1777.8, 1903.0, 2028.3, 2153.5,
    2278.8, 2404.0, 2529.3, 2654.5, 2779.8,
    2905.1, 3030.3, 3155.6, 3280.8, 3406.1,
    3531.3, 3656.6, 3781.8, 3907.1, 4032.3,
    4157.6, 4282.8, 4408.1, 4533.3, 4658.6,
    4783.8, 4909.1, 5034.3, 5159.6, 5284.8,
    5410.1, 5535.4, 5660.6, 5785.9, 5911.1,
    6036.4, 6161.6, 6286.9, 6412.1, 6537.4,
    6662.6, 6787.9, 6913.1, 7038.4, 7163.6,
    7288.9, 7414.1, 7539.4, 7664.6, 7789.9,
    7915.2, 8040.4, 8165.7, 8290.9, 8416.2,
    8541.4, 8666.7, 8791.9, 8917.2, 9042.4,
    9167.7, 9292.9, 9418.2, 9543.4, 9668.7, 
    9793.9, 9919.2, 10044.0, 10170.0, 10295.0,
    10420.0, 10545.0, 10671.0, 10796.0, 10921.0,
    11046.0, 11172.0, 11297.0, 11422.0, 11547.0,
    11673.0, 11798.0, 11923.0, 12048.0, 12174.0,
    12299.0, 12424.0, 12549.0, 12675.0, 12800.0,
};

static double MFX_only[100] = 
{
500.0 ,  500.0 ,  500.0 ,  500.0 ,  500.0 ,
500.0 ,  500.0 ,  500.0 ,  500.0 ,  500.0 ,
500.0 ,  500.0 ,  500.0 ,  500.0 ,  500.0 ,
500.0 ,  500.0 ,  500.0 ,  500.0 ,  500.0 ,
500.0 ,  500.0 ,  383.3468, 383.3468, 383.3457,
383.3441, 383.3419, 383.3391, 383.3354, 383.3312,
383.3162, 383.3081, 383.2996, 383.2905, 383.2809,
383.2709, 383.2613, 383.2512, 382.1419, 381.5325,
381.5318, 381.531 , 381.53  , 381.5287, 381.5272,
381.5254, 381.5234, 381.5212, 381.5187, 381.5159,
381.5131, 381.5098, 381.5068, 381.5032, 381.4998,
381.4963, 381.4925, 381.4891, 381.4852, 381.482 ,
381.4782, 381.4747, 381.4715, 381.4678, 381.4642,
381.4616, 381.4581, 381.4329, 381.4096, 381.3756,
381.3429, 381.3229, 381.2937, 381.2645, 381.237 ,
381.2237, 381.199 , 381.1753, 381.1515, 381.1446,
381.1244, 381.1046, 381.0856, 381.0841, 381.0683,
381.0521, 381.0357, 381.0223, 381.0273, 381.0143,
381.0026, 380.9907, 380.9854, 380.9915, 380.9825,
380.9737, 380.9649, 380.9689, 380.9733, 380.966 ,
};

static double XRT_only[100] = 
{
0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,
0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,
0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,
0.0 , 0.0 , 0.0 , 0.0 , 0.0 ,
377.309 , 377.311 , 377.314 , 377.314 , 377.319 ,
377.327 , 377.338 , 377.352 , 377.37  , 377.39  ,
378.517 , 378.519 , 378.521 , 378.525 , 378.532 ,
378.986 , 378.987 , 379.359 , 379.36  , 379.361 ,
379.362 , 379.364 , 379.367 , 379.371 , 379.375 ,
379.381 , 379.388 , 379.471 , 379.621 , 379.777 ,
379.978 , 380.162 , 380.324 , 380.517 , 382.601 ,
382.965 , 383.356 , 383.688 , 384.089 , 384.403 ,
384.79  , 385.141 , 385.453 , 385.832 , 386.761 ,
387.028 , 387.423 , 387.801 , 387.968 , 388.328 ,
388.674 , 388.796 , 389.092 , 389.394 , 389.677 ,
389.704 , 389.944 , 390.179 , 390.416 , 390.355 ,
390.541 , 390.729 , 390.907 , 390.771 , 390.905 ,
391.049 , 391.195 , 391.307 , 391.083 , 391.188 ,
391.278 , 391.369 , 391.356 , 391.144 , 391.203 ,
391.259 , 391.315 , 391.163 , 391.007 , 391.045 ,
};

static double Prefocus[100] = 
{
500.0,  500.0,  500.0,  500.0,  500.0,
500.0,  500.0,  500.0,  500.0,  500.0,
500.0,  500.0,  500.0,  500.0,  500.0,
500.0,  500.0,  500.0,  500.0,  500.0,
500.0,  385.579 , 385.575 , 385.575 , 385.57  ,
385.563 , 385.552 , 385.539 , 385.521 , 385.502 ,
385.431 , 385.394 , 385.355 , 385.313 , 385.269 ,
385.224 , 385.181 , 382.5878, 382.5865, 382.5846,
382.5821, 382.5788, 382.5747, 382.5695, 382.5637,
382.5566, 382.5487, 382.5401, 382.5301, 382.5194,
382.5082, 382.4955, 382.4837, 382.4698, 382.4566,
382.4429, 382.3781, 382.2725, 382.155 , 382.0535,
381.9403, 381.8344, 381.7374, 381.6308, 381.4362,
381.3528, 381.2519, 381.1569, 381.0952, 381.0066,
380.9229, 380.8726, 380.8   , 380.7284, 380.662 ,
380.6304, 380.5722, 380.517 , 380.4622, 380.4467,
380.401 , 380.3565, 380.3145, 380.3114, 380.2767,
380.2414, 380.206 , 380.1772, 380.1881, 380.1604,
380.1356, 380.1108, 380.0995, 380.1126, 380.0937,
380.0755, 380.0573, 380.0657, 380.0748, 380.0598,
};
#endif








































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































