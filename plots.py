import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import lines, colors, ticker
import seaborn as sns
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
#sys.path.append('../externals/gfz_cygnss/')
import utils.mathematics as mat

deg = 1 # grid resolution (publication: 1)

#xx, yy, gridded_y_pred = mat.average_to_grid2(sp_lon[:], sp_lat[:], y_pred[:], resolution=deg)
#xx, yy, gridded_bias = mat.average_to_grid2(sp_lon[:], sp_lat[:], y_pred[:] - y_true[:], resolution=deg)

grid_lon = np.arange(-180, 181, deg)
grid_lat = np.arange(-90, 91, deg)

def make_scatterplot(y_true, y_pred):
    ymin = 2.5
    ymax = 25.0

    fig=plt.figure()
    ax=fig.add_subplot(111)

    img=ax.hexbin(y_true, y_pred, cmap='viridis', norm=colors.LogNorm(vmin=1, vmax=25000), mincnt=1)
    clb=plt.colorbar(img)
    clb.set_ticks([1, 10, 100, 1000, 10000])
    clb.set_ticklabels([r'$1$', r'$10$', r'$10^2$', r'$10^3$', r'$10^4$'])
    clb.set_label('Samples in bin')
    clb.ax.tick_params()

    ax.set_xlabel('ERA5 wind speed (m/s)')
    ax.set_ylabel('Predicted wind speed (m/s)')

    ax.plot(np.linspace(0, 30), np.linspace(0, 30), 'w:')

    ax.set_ylim(ymin, 25)
    ax.set_xlim(ymin, 25)

    ax.set_xticks([5, 10, 15, 20, 25])
    ax.set_xticklabels([5, 10, 15, 20, 25])
    ax.set_yticks([5, 10, 15, 20, 25])
    ax.set_yticklabels([5, 10, 15, 20, 25])

    fig.tight_layout()
    plt.savefig(f'{os.path.dirname(__file__)}/plots/scatter.png')


def make_histogram(y_true, y_pred):
    fig=plt.figure()
    ax=fig.add_subplot(111)

    sns.histplot(y_true, ax=ax, color='C7', label='ERA5 wind speed (m/s)')
    sns.histplot(y_pred, ax=ax, color='C2', label='Predicted wind speed (m/s)')

    ax.legend(fontsize=12)

    ax.set_xticks([5, 10, 15, 20, 25])
    ax.set_xticklabels([5, 10, 15, 20, 25])
    ax.set_xlabel('ERA5 wind speed (m/s)')
    plt.savefig(f'{os.path.dirname(__file__)}/plots/histo.png')


def era_average(y_true, sp_lon, sp_lat):
    xx, yy, gridded_y_true = mat.average_to_grid2(sp_lon[:], sp_lat[:], y_true[:], resolution=deg)
    proj = ccrs.PlateCarree(180)
    
    fig, ax = plt.subplots(1, 1, figsize=(6,4), gridspec_kw=dict(hspace=0.05, wspace=0.1), subplot_kw=dict(projection=proj))
    cmap = ax.contourf(grid_lon[:], grid_lat[::-1][:], gridded_y_true[:].T, levels=60, transform=proj, antialiased=False, cmap='magma')
    ax.coastlines()
    gl = ax.gridlines(crs=proj, draw_labels=True, linewidth=0, color='gray', alpha=0.5, linestyle=':')
    gl.top_labels = False
    gl.right_labels= False
    clb = plt.colorbar(cmap, ax=ax, orientation='horizontal', shrink=1, label='Average ERA5 wind speed (m/s)')

    clb.set_ticks(np.arange(2.5, 18, 2.5))
    clb.ax.tick_params(labelsize=8)

    gl.xlabel_style = {'size': 8, 'color': 'black'}
    gl.ylabel_style = {'size': 8, 'color': 'black'}

    plt.savefig(f'{os.path.dirname(__file__)}/plots/era_average.png')

def rmse_average(y_true, y_pred, sp_lon, sp_lat):
    xx, yy, gridded_rmse = mat.average_to_grid2(sp_lon[:], sp_lat[:], np.abs(y_pred[:] - y_true[:]), resolution=deg)
    proj = ccrs.PlateCarree(180)
    fig, ax = plt.subplots(1, 1, figsize=(6,4), gridspec_kw=dict(hspace=0.05, wspace=0.1), subplot_kw=dict(projection=proj))
    cmap = ax.contourf(grid_lon[:], grid_lat[::-1][:], gridded_rmse[:].T, levels=60, transform=proj, antialiased=False, cmap='viridis')
    ax.coastlines()
    gl = ax.gridlines(crs=proj, draw_labels=True, linewidth=0, color='gray', alpha=0.5, linestyle=':')
    gl.top_labels = False
    gl.right_labels= False
    clb = plt.colorbar(cmap, ax=ax, orientation='horizontal', shrink=1, label='Average RMSE (m/s)')

    clb.set_ticks(np.arange(0, np.nanmax(gridded_rmse)+1, 1.0))
    clb.ax.tick_params(labelsize=8)

    gl.xlabel_style = {'size': 8, 'color': 'black'}
    gl.ylabel_style = {'size': 8, 'color': 'black'}


def today_longrunavg(df_mockup, y_bins):
    
    fig=plt.figure(figsize=(10,4))
    ax=fig.add_subplot(111)

    sns.barplot(data=df_mockup, x='bins', y='rmse', hue='time', ax=ax)
    ax.legend()

    ax.set_xlabel('ERA5 wind speed (m/s)')
    ax.set_ylabel('RMSE (m/s)')

    ax.set_xticks(range(len(y_bins)))
    ax.set_xticklabels([f'< {yy} m/s' for yy in y_bins])

    plt.savefig(f'{os.path.dirname(__file__)}/plots/today_longrunavg.png')

def today_longrunavg_bias(df_mockup, y_bins):

    fig=plt.figure(figsize=(10,4))
    ax=fig.add_subplot(111)

    sns.barplot(data=df_mockup, x='bins', y='bias', hue='time', ax=ax)
    ax.legend()

    ax.set_xlabel('ERA5 wind speed (m/s)')
    ax.set_ylabel('Bias (m/s)')

    ax.set_xticks(range(len(y_bins)))
    ax.set_xticklabels([f'< {yy} m/s' for yy in y_bins])
    
    plt.savefig(f'{os.path.dirname(__file__)}/plots/today_long_bias.png')

def sample_counts(df_rmse, y_bins):

    fig=plt.figure(figsize=(10,4))
    ax=fig.add_subplot(111)
    sns.barplot(data=df_rmse, x='bins', y='counts', ax=ax)
    ax.set_xlabel('ERA5 wind speed (m/s)')
    ax.set_ylabel('Sample counts')

    ax.set_xticks(range(len(y_bins)))
    ax.set_xticklabels([f'< {yy} m/s' for yy in y_bins])

    plt.savefig(f'{os.path.dirname(__file__)}/plots/sample_counts.png')

def rmse_bins_era(df_rmse, y_bins):

    fig=plt.figure(figsize=(10,4))
    ax=fig.add_subplot(111)
    sns.barplot(data=df_rmse, x='bins', y='rmse', ax=ax)
    ax.set_xlabel('ERA5 wind speed (m/s)')
    ax.set_ylabel('RMSE (m/s)')

    ax.set_xticks(range(len(y_bins)))
    ax.set_xticklabels([f'< {yy} m/s' for yy in y_bins])

    plt.savefig(f'{os.path.dirname(__file__)}/plots/rmse_bins_era.png')

def bias_bins_era(df_rmse, y_bins):

    fig=plt.figure(figsize=(10,4))
    ax=fig.add_subplot(111)
    sns.barplot(data=df_rmse, x='bins', y='bias', ax=ax)
    ax.set_xlabel('ERA5 wind speed (m/s)')
    ax.set_ylabel('Bias (m/s)')

    ax.set_xticks(range(len(y_bins)))
    ax.set_xticklabels([f'< {yy} m/s' for yy in y_bins])
 
    plt.savefig(f'{os.path.dirname(__file__)}/plots/bias_bins_era.png')