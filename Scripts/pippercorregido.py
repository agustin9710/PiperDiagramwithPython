#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import os, math
import matplotlib.pyplot as plt
import imageio


# In[2]:


#nos dirigimos al sitio del formato
img = imageio.imread("../Figures/PiperCompleto.png")


# In[3]:


#importamos los datos
datosQuimica = pd.read_excel('../Xls/HidroquimicaIglesia.xlsx')
datosQuimica.head()


# In[4]:


#diccionario de iones divido valencia
iones = {
'HCO3': 61.0168, 'CO3' : 60/2, 'Cl' : 35.453, 'SO4': 96.06/2,
'Na' : 23, 'Ca' : 40.078/2, 'Mg' : 24.035/2, 'K'  : 39.0983
}

#generamos las columnas de concentraciones equivalentes
for ion in iones.keys():
    datosQuimica[str(ion)+'_meq'] = datosQuimica[ion]/iones[ion]
    
datosQuimica.head()


# In[5]:


# calcula el error 
datosQuimica['antiones'] = datosQuimica['SO4_meq'] + datosQuimica['HCO3_meq'] + datosQuimica['Cl_meq']+datosQuimica['CO3_meq']
datosQuimica['cantiones'] =datosQuimica['Mg_meq'] +datosQuimica['Na_meq'] +   datosQuimica['Ca_meq'] + datosQuimica['K_meq']
datosQuimica['error'] = (datosQuimica['antiones'] - datosQuimica['cantiones'])/(datosQuimica['antiones'] + datosQuimica['cantiones'])
datosQuimica.head()


# In[6]:


#normalizamos los aniones
datosQuimica['SO4_norm'] = datosQuimica['SO4_meq'] / (datosQuimica['SO4_meq'] +
                            datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']+datosQuimica['Cl_meq']) * 100
datosQuimica['HCO3_CO3_norm'] = (datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']) / (datosQuimica['SO4_meq'] +
                            datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']+datosQuimica['Cl_meq']) * 100
datosQuimica['Cl_norm'] = datosQuimica['Cl_meq'] / (datosQuimica['SO4_meq'] +
                            datosQuimica['HCO3_meq']+datosQuimica['CO3_meq']+datosQuimica['Cl_meq']) * 100

#normalizamos los cationes
datosQuimica['Mg_norm'] = datosQuimica['Mg_meq'] / (datosQuimica['Mg_meq'] +
                            datosQuimica['Ca_meq']+datosQuimica['K_meq']+datosQuimica['Na_meq']) * 100
datosQuimica['Na_K_norm'] = (datosQuimica['K_meq']+datosQuimica['Na_meq']) / (datosQuimica['Mg_meq'] +
                            datosQuimica['Ca_meq']+datosQuimica['K_meq']+datosQuimica['Na_meq']) * 100
datosQuimica['Ca_norm'] = datosQuimica['Ca_meq'] / (datosQuimica['Mg_meq'] +
                            datosQuimica['Ca_meq']+datosQuimica['K_meq']+datosQuimica['Na_meq']) * 100
datosQuimica.head()
datosQuimica.to_excel('../Output/datosmeq.xls')


# In[7]:


#funcion de las coordenadas
def coordenada(Ca,Mg,Cl,SO4,Label):
    xcation = 40 + 360 - (Ca + Mg / 2) * 3.6
    ycation = 40 + (math.sqrt(3) * Mg / 2)* 3.6
    xanion = 40 + 360 + 100 + (Cl + SO4 / 2) * 3.6
    yanion = 40 + (SO4 * math.sqrt(3) / 2)* 3.6
    xdiam = 0.5 * (xcation + xanion + (yanion - ycation) / math.sqrt(3))
    ydiam = 0.5 * (yanion + ycation + math.sqrt(3) * (xanion - xcation))
    #print(str(xanion) + ' ' + str(yanion))
    c=np.random.rand(3,1).ravel()
    c = np.sort(c)
    listagraph=[]
    listagraph.append(plt.scatter(xcation,ycation,zorder=1,c=c, s=60, edgecolors='#4b4b4b',label=Label))
    listagraph.append(plt.scatter(xanion,yanion,zorder=1,c=c, s=60, edgecolors='#4b4b4b'))
    listagraph.append(plt.scatter(xdiam,ydiam,zorder=1,c=c, s=60, edgecolors='#4b4b4b'))
    return listagraph


# In[8]:


plt.figure(figsize=(20,15))
plt.imshow(np.flipud(img),zorder=0)
for index, row in datosQuimica.iterrows():
    coordenada(row['Ca_norm'],row['Mg_norm'],row['Cl_norm'],row['SO4_norm'],index)
plt.ylim(0,830)
plt.xlim(0,900)
plt.axis('off')
plt.legend(loc='upper right',prop={'size':10}, frameon=False, scatterpoints=1)

plt.savefig('../Output/Piper.png')
plt.savefig('../Output/Piper.pdf')
plt.savefig('../Output/Piper.svg')


# In[ ]:




