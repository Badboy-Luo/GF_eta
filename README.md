# GF_eta

## Introduction
The geometric phase is a global measure of the spatial geometry of an acoustic or seismic field, making it a highly sensitive metric to changes in the wave supporting medium.
This GF_eta package shows how to calculate the geometry phase of a seismic field by reconstructing the ground Green's function through seismic noise recordings.

cc.sh: A MSNoise job script. We use the MSNoise software to cross-correlate continuous seismic data. The output are daily noise correlation functions (NCFs) between every two seismic stations, approximating Green's functions between every two sites.

eta.py: Calculating temporal changes in geometric phase ($\Delta \eta$) based on daily NCFs.

## Requirements
This package should be run in a Python environment with the following required modules and recommended versions:

Python = 3.7 

MSNoise = 1.6.3 (A seismic data processing tool: http://msnoise.org/doc)

obspy = 1.3.1

matplotlib = 3.5.3

numpy = 1.17.0

scipy = 1.7.3

tqdm = 4.66.1



## Usage

## Authors and acknowledgment
