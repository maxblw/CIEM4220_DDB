# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 13:50:27 2025

@author: rrodriguesbend
"""
# %% packages 
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from read_swan_1d_spectrum import read_swan_1d_spectrum
import pandas as pd
# %% Reading data 
data = scipy.io.loadmat("Result.mat")

frequencies, vadens, dir_mean, dspred = read_swan_1d_spectrum("swan_specout.txt")

df = pd.read_csv('swan_transect1.tab', 
                 delim_whitespace=True, 
                 comment='%', 
                 header=None,
                 names=['XP', 'YP', 'HSIGN', 'RTP', 'BOTLEV', 'PDIR'])

# %% Ploting Map 
# Variables 
Xp   = data['Xp']    
Yp   = data['Yp']    
Hs  = data['Hsig']  
Tp   = data['RTpeak']  
Dir   = data['PkDir']  
Tm01   = data['Tm01']  
Tm02   = data['Tm02']  
Botlev   = data['Botlev']  

P1 = (772101, 4903042)

# 
theta_rad = np.radians((270 - Dir) % 360)
Hmx = Hs * np.cos(theta_rad)
Hmy = Hs * np.sin(theta_rad)

# 
fig, ax = plt.subplots(figsize=(10, 8))
c = ax.pcolormesh(Xp, Yp, Hs, shading='auto', cmap='jet')
skip = (slice(None, None, 5), slice(None, None, 15))  
q = ax.quiver(Xp[skip], Yp[skip], Hmx[skip], Hmy[skip], color='k', scale=75)
ax.scatter(P1[0], P1[1], facecolor='yellow', edgecolors='black', marker='^', 
            label='S1', s=200)  

ax.annotate('S1', xy=(P1[0], P1[1]), xytext=(5, -10),
            textcoords="offset points", fontsize=12, color='Black', weight='bold')

plt.plot(df['XP'], df['YP'], 'k', linewidth = 3)

cbar = plt.colorbar(c, ax=ax)
cbar.set_label('Hm0 [m]')
ax.set_xlabel('X coordinate [m]')
ax.set_ylabel('Y coordinate [m]')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()

# %% Spectrum 

plt.figure()
plt.plot(frequencies, vadens, marker='o')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Energy [m²/Hz]')
plt.title('1D Frequency Spectrum')
plt.grid()
plt.show()

# %% Transect 
# Dealing with transect distances
dx = np.diff(df['XP'])
dy = np.diff(df['YP'])
distances = np.sqrt(dx**2 + dy**2)  
distances = np.insert(distances, 0, 0)
df['Length'] = np.cumsum(distances)

plt.figure(figsize=(8,5))
plt.plot(df['Length'] , df['HSIGN'], marker='o')
plt.xlabel('Length [m]')
plt.ylabel('Significant Wave Height Hsig (m)')
plt.ylim(2.5, 3.75)
plt.title('Hsig along the Curve')
plt.grid(True)
plt.show()
