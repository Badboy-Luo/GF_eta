# GF_eta   

<img src="logo/newfos_logo.png" width="30%" align='middle'>


## Introduction

The geometric phase is a global measure of the spatial geometry of an acoustic or seismic field, making it a highly sensitive metric to changes in the ground properties.
The GF_eta package shows how to calculate the geometry phase of a seismic field by reconstructing the ground Green's function (GF) through seismic noise cross-correlations.

Our team is belong to the New Frontiers of Sound ([NewFoS](https://newfos.arizona.edu/)) Science and Technology Center, which is funded by the National Science Foundation and is based at the University of Arizona in Tucson.


## What's inside the package

`cc.sh`: A MSNoise job script. We use the [MSNoise](http://msnoise.org/doc) (A seismic data processing tool) to cross-correlate continuous seismic data. 
The output are daily noise correlation functions (NCFs) between every two seismic stations, approximating GFs between every two sites.
You can customize the control parameters by following the [instruction](http://msnoise.org/doc/workflow/001_msnoise_admin.html).
We directly provide the output in `NCFs`.

`eta.py`: A Python script to calculate $\Delta \eta$ by using daily NCFs. The output include a time-frequency plot of $\Delta \eta(\omega,t)$, and $\Delta \eta$ time series along with local surface air temperature.

`NCFs`: Daily NCFs between every two seismic station recordings. All daily NCFs have been stacked every 10 days to enhance the reconstruction of GFs.

`ERA5`: The ERA5 environmental datasets (surface air temperature, surface pressure, and snow depth) at the local study area in Iceland.





## Methodology

We follow this criteria to calculate the $\Delta \eta (\omega)$. The complex state vector $C_{t}(\omega)$ can be built by involving NCFs as follows:

$$ C_t (\omega) = \frac{1}{ \sqrt{ \sum^{N} \textbf{Re}(n)^2 + \textbf{Im}(n)^2 } } 
	\left(
		\begin{array}{c}
			C^{1}e^{i\phi_{1}}	\\
			C^{2}e^{i\phi_{2}} \\
			... \\
			C^{N}e^{i\phi_{n}}		
		\end{array}
	\right) , $$
 
where the complex state vector at a certain day $t$, $C_t(\omega)$, is a function of frequency $\omega$ and consists of $N$ components. We apply the Fast Fourier Transform to each component of $C^N e^{i\phi_{n}}$, which includes its both real ($\textbf{Re}$) and imaginary ($\textbf{Im}$) parts. The denominator is to normalize all magnitudes to scale all components at the same level.

The change in geometric phase ($\Delta \eta$) of daily $C_{t}$ with respect to the reference $C_{ref}$ can be represented by their angle difference: 
 
$$ \Delta \eta(\omega,t) \approx arcos \left[ \textbf{Re}\left( C_{ref}^* \cdot C_t \right) \right]  \quad and \quad \Delta \eta \in [0,\pi] , $$

We measure the angle difference by taking the $arcos$ function of the real part of the dot product between these two complex vectors. $^*$ denotes the complex conjugate.




## Requirements

The `eta.py` script should be run in a Python environment with the following required modules and recommended versions:

Python 3.7 

obspy 1.3.1

matplotlib 3.5.3

numpy 1.17.0

scipy 1.7.3

tqdm 4.66.1

Please [install](http://msnoise.org/doc/installation.html) the MSNoise properly if you want to start from seismic data cross-correlations and output NCFs:

MSNoise 1.6.3 



## Usage


## Citation
Our latest manuscript is being submitted:

*Luo, B., Deymier, P., Beck, S., Runge, K., Huettmann, F., DeVaughn, S., Latypov, M. (2024). Geometric phase sensing of environmental changes based on seismic noise: An application from Iceland.*


## Acknowledgment





