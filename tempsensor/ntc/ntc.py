import numpy as np
import pylab as pl

K0 = 273.15
def fit_Steinhart_Hart(T,data_fit,cfit=3):
    """
    Fits data of a sensor to a Steinhart-Hart type of equation.

    Parameters
    ----------
    T : TYPE
        DESCRIPTION.
    data_fit : TYPE
        DESCRIPTION.
    cfit : TYPE, optional
        DESCRIPTION. The default is 3.

    Returns
    -------
    fit : TYPE
        DESCRIPTION.

    """
    K = T + K0
    K_1 = 1/K
    dlog = np.log(data_fit)
    P = np.polyfit(dlog,K_1,cfit)
    K_1_fit = np.polyval(P,dlog)
    T_fit = 1/K_1_fit - K0
    fit = {'P':P,'T_fit':T_fit,'dlog':dlog,'K_1':K_1,'K_1_fit':K_1_fit}
    return fit


def print_coeffs(fit):
    P = fit['P']
    for i in range(len(P)):
        print('a[{:d}]: {:e}'.format(i,P[-i-1]))


def get_T_Steinhart_Hart(data,P):
    """
    With the Steinhart-Hart coefficients in P and the data the temperature is calculated.

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    P : TYPE
        DESCRIPTION.

    Returns
    -------
    T_fit : TYPE
        Temperature of the sensor.

    """
    dlog = np.log(data)    
    K_1_fit = np.polyval(P,dlog)
    T_fit = 1/K_1_fit - K0
    return T_fit
    


if __name__ == "__main__":
    fname ='ntc_ref.csv'
    #fname ='ntc_ref_Rparinf.csv'
    data = np.genfromtxt (fname, delimiter=",")
    T = data[:,0]
    dfit = data[:,-1]
    pl.figure(1)
    pl.clf()
    pl.plot(T,dfit)

    npoly = 4
    fit = fit_Steinhart_Hart(T,dfit,cfit=npoly)
    dcount = 0.5
    T1 = get_T_Steinhart_Hart(dfit+dcount,fit['P'])
    T2 = get_T_Steinhart_Hart(dfit-dcount,fit['P'])
    T_fit_diff = T1-T2

    K_1 = fit['K_1']
    K_1_fit = fit['K_1_fit']
    T_fit = fit['T_fit']
    dlog = fit['dlog']
    dlog = fit['T_fit']
    data_fit = dfit
    pl.figure(2)
    pl.clf()
    
    pl.subplot(2,2,1)
    pl.plot(K_1,dlog)
    pl.plot(K_1_fit,dlog)

    pl.subplot(2,2,2)
    pl.plot(T,T_fit_diff)
    pl.xlabel('Data fit')
    pl.ylabel('dT [K]')
    pl.ylim([-.01,.01])

    pl.subplot(2,2,3)
    pl.plot(data_fit,T)
    pl.plot(data_fit,T_fit)
    pl.xlabel('Data fit')
    pl.ylabel('T [degC]')

    pl.subplot(2,2,4)
    pl.plot(T,data_fit)
    pl.plot(T_fit,data_fit)
    pl.ylabel('Data fit')
    pl.xlabel('T [degC]')
    
    pl.show()

