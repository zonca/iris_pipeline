
/*-----------------------------------------------------------------------------
 * Includes
 *---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include "fitsio.h"
#include <math.h>
#include <string.h>

float* uptheramp (int* arr, int* time, int xlim, int ylim, int zlim ) {
    
    /* Local Variables */
     
    int i, j, k, nelem, sz;
    float *new_arr;
    double tisi=0;
    double ti=0;
    double si=0;
    double ti2=0;
    double a;
    double xymult;
    double x2;
    
    /* Elements  */
    nelem=ylim*zlim;
    
    /* Memory Allocation  */
    new_arr = (float*) malloc(nelem* sizeof(float));
        
    
    for (i = 0; i<nelem; i++) {
	tisi=0;
	ti=0;
	si=0;
	ti2=0;   
        for (j = 0; j<xlim; j++) {
	    
	    xymult=time[j]*arr[i+j*ylim*zlim];
	    x2=time[j]*time[j];
	    tisi=tisi+xymult;

	    ti=ti+time[j];
	    si=si+arr[i+j*ylim*zlim];
	    ti2=ti2+x2; 	    
	         
        }    
	a=(((xlim*(tisi)) - (ti*si)) / ((xlim*ti2)-(ti*ti))) * (time[xlim-1]-time[0]);
	new_arr[i]=a;  
    }           
    return new_arr;

}

float* mcds (int* arr, int* time, int xlim, int ylim, int zlim, int num_coadd ) {
    
    /* Local Variables */
     
    int i, j, k, nelem;
    float *new_arr;
    double a;
    double sum_coadd1,sum_coadd2,avg_coadd1,avg_coadd2;
    /* Elements  */
    nelem=ylim*zlim;
    
    /* Memory Allocation  */
    new_arr = (float*) malloc(nelem* sizeof(float));
        
    
    for (i = 0; i<nelem; i++) {
	sum_coadd1=0;
	sum_coadd2=0;
        for (j = 0; j<(num_coadd); j++) {
	    	    sum_coadd1=sum_coadd1+arr[i+j*ylim*zlim];	         
        }    
        for (j = xlim-1; j>((xlim-1)-num_coadd); j--) {
	    	    sum_coadd2=sum_coadd2+arr[i+j*ylim*zlim];	         
        }         
	avg_coadd1=sum_coadd1/num_coadd;
	avg_coadd2=sum_coadd2/num_coadd;
	
	a=avg_coadd2-avg_coadd1;
	new_arr[i]=a;  
    }           
    return new_arr;

}

float* nonlin_corr (int* arr, int* time, int xlim, int ylim, int zlim, int x_0, int y_0, float* c0, float* c1, float* c2, float* c3, float* c4) {
    
    /* Local Variables */
     
    int i, j, k, nelem, arrelem, fullelem, x;
    fitsfile *c0ptr,*c1ptr,*c2ptr,*c3ptr,*c4ptr;
    float y,c00,c11,c22,c33,c44,kaka;
    float *new_arr;
    int status = 0;
    int hdutype, naxis;
    long naxes[3], totpix, fpixel[2];

    nelem=ylim*zlim;
    arrelem=xlim*ylim*zlim;
    fullelem=2048*2048;
    fpixel[0]=1;
    fpixel[1]=1;

    
    //c0 = (float *) malloc(fullelem* sizeof(float));
    //c1 = (float *) malloc(fullelem* sizeof(float));
    //c2 = (float *) malloc(fullelem* sizeof(float));
    //c3 = (float *) malloc(fullelem* sizeof(float));
    //c4 = (float *) malloc(fullelem* sizeof(float)); 
    

    
    //fits_open_file(&c0ptr,"/home/arun/coeff_nonlin/coeff0.fits", READONLY, &status);
    //fits_open_file(&c1ptr,"/home/arun/coeff_nonlin/coeff1.fits", READONLY, &status);
    //fits_open_file(&c2ptr,"/home/arun/coeff_nonlin/coeff2.fits", READONLY, &status);
    //fits_open_file(&c3ptr,"/home/arun/coeff_nonlin/coeff3.fits", READONLY, &status);
    //fits_open_file(&c4ptr,"/home/arun/coeff_nonlin/coeff4.fits", READONLY, &status);
    
    //fits_read_pix(c0ptr, TFLOAT, fpixel, fullelem,0, c0,0, &status); 
    //fits_read_pix(c1ptr, TFLOAT, fpixel, fullelem,0, c1,0, &status); 
    //fits_read_pix(c2ptr, TFLOAT, fpixel, fullelem,0, c2,0, &status); 
    //fits_read_pix(c3ptr, TFLOAT, fpixel, fullelem,0, c3,0, &status); 
    //fits_read_pix(c4ptr, TFLOAT, fpixel, fullelem,0, c4,0, &status); 
    
    /* Elements  */
    

    /* Memory Allocation  */
    new_arr = (float*) malloc(arrelem* sizeof(float));

    //for (i = 0; i<2048; i++) {
		//for (j = 0; j<2048; j++) {
			//printf("%d i %d j  output \n",i,j);
			//c0_arr[i][j]=c0[j+i*2048];
			//c1_arr[i][j]=c1[j+i*2048];
			//c2_arr[i][j]=c2[j+i*2048];
			//c3_arr[i][j]=c3[j+i*2048];
			//c4_arr[i][j]=c4[j+i*2048];		
			//printf("%f\n", c0_arr[i+1][j+1]);	
		//}	
	//}		      
    //printf("%f output \n", c0_arr[10][10]);	

	//printf("%d arrelem  %d xlim %d ylim %d zlim \n", arrelem,xlim,ylim,zlim);	
    for (i = 0; i<zlim; i++) {
		for (j = 0; j<ylim; j++) {
			for (k = 0; k<xlim; k++) {
				
				c00=c0[j+i*2048];
				c11=c1[j+i*2048];
				c22=c2[j+i*2048];
				c33=c3[j+i*2048];
				c44=c4[j+i*2048];
				//printf("%d\n",arr[i+j*ylim+k*ylim*zlim]);
				x=arr[i+j*ylim+k*ylim*zlim];
				//printf("%d x \n", x);	
				y=(1+c00+(c11*x)+(c22*pow(x,2))+(c33*pow(x,3))+(c44*pow(x,4)))*x;
				new_arr[i+j*ylim+k*ylim*zlim] = y;
				//printf("%f y \n", y);
			    
	    	   
			}
	    }	    
    }   
   // for (i = 0; i<100; i++) { 
	//printf("%f pop\n",c1[i]);
	//}	       
    return new_arr;

}
