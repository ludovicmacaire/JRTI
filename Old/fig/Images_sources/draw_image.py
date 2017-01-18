import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.cm as cm
from matplotlib import colors

def draw_cfa(image_data, label_str, label_coords=False):
    # draw a cfa or cfa derivative image
    for (y,x),label in np.ndenumerate(image_data):
        # draw shapes according to CFA pixel subsets
        pad = 0.05  # blank around shape
        label = '$'+eval(label_str)
        if label_coords:
            label += '_{'+str(x)+','+str(y)+'}'
        label += '$'
        if ((y+x)%2 == 0):  # G locations
            if (y%2 == 0):  # G,R locations
                dr = (1-2*pad)/(2+math.sqrt(2)) # octogons
            else:   # G,B locations
                dr = -0.3   # negative dr: square with rounded edges
        else:
            if (y%2 == 0):  # R locations
                dr = 0.5-pad    # diamonds
            else:   # B locations
                dr = 0.   # squares
        ax1.text(x,y,label,ha='center',va='center',fontsize=25,color='white')
        x0, y0, x1, y1 = x-0.5+pad, y-0.5+pad,x+0.5-pad, y+0.5-pad,
        if (dr >= 0):
            path_data = [
                (mpath.Path.MOVETO, [x0+dr, y0]),
                (mpath.Path.LINETO, [x1-dr, y0]),
                (mpath.Path.LINETO, [x1,  y0+dr]),
                (mpath.Path.LINETO, [x1 ,  y1-dr]),
                (mpath.Path.LINETO, [x1-dr,  y1]),
                (mpath.Path.LINETO, [x0+dr,  y1]),
                (mpath.Path.LINETO, [x0, y1-dr]),
                (mpath.Path.LINETO, [x0, y0+dr]),
                (mpath.Path.CLOSEPOLY, [x0, y0+dr])
            ]   # see http://matplotlib.org/examples/shapes_and_collections/artist_reference.html
        else:
            dr = -dr
            path_data = [
                (mpath.Path.MOVETO, [x0+dr, y0]),
                (mpath.Path.LINETO, [x1-dr, y0]),
                (mpath.Path.CURVE3, [x1,  y0]), (mpath.Path.CURVE3, [x1,  y0+dr]),
                (mpath.Path.LINETO, [x1 ,  y1-dr]),
                (mpath.Path.CURVE3, [x1,  y1]), (mpath.Path.CURVE3, [x1-dr,  y1]),
                (mpath.Path.LINETO, [x0+dr,  y1]),
                (mpath.Path.CURVE3, [x0,  y1]), (mpath.Path.CURVE3, [x0,  y1-dr]),
                (mpath.Path.LINETO, [x0, y0+dr]),
                (mpath.Path.CURVE3, [x0,  y0]), (mpath.Path.CURVE3, [x0+dr,  y0]),
                (mpath.Path.CLOSEPOLY, [x0+dr, y0])
            ]   # see http://matplotlib.sourcearchive.com/documentation/0.99.1.2-3ubuntu1/classmatplotlib_1_1patches_1_1BoxStyle_1_1Square_1_1Round_32adadb5b3da4fd5e86687fd3751787e.html#32adadb5b3da4fd5e86687fd3751787e
        codes, vertices = zip(*path_data)
        path = mpath.Path(vertices, codes)
        patch = mpatches.PathPatch(path,fill=False,edgecolor='yellow',facecolor=None)
        ax1.add_patch(patch)


# parameters
image_size = np.array([5,5])
image_data = {
    'I^CFA': np.tile([[255,123],[5,255]],image_size/2+1)[:image_size[0],:image_size[1]],
    'S^R': np.tile([[150,123],[150,150]],image_size/2+1)[:image_size[0],:image_size[1]],
    'S^G': np.tile([[123,150],[150,123]],image_size/2+1)[:image_size[0],:image_size[1]],
    'S^B': np.tile([[150,150],[123,150]],image_size/2+1)[:image_size[0],:image_size[1]],
    'S^G,R': np.tile([[123,150],[150,150]],image_size/2+1)[:image_size[0],:image_size[1]],
    'S^G,B': np.tile([[150,150],[150,123]],image_size/2+1)[:image_size[0],:image_size[1]],
    'I^CFA_x': 150*np.ones(image_size),
    'I^CFA_y': 150*np.ones(image_size)
}
labels = {
    'I^CFA': ['G','R','B','G'],
    'S^R': ['\ ','R','\ ','\ '],
    'S^G': ['G','\ ','\ ','G'],
    'S^B': ['\ ','\ ','B','\ '],
    'S^G,R': ['G','\ ','\ ','\ '],
    'S^G,B': ['\ ','\ ','\ ','G'],
    'I^CFA_x': ['I^R_x','I^G_x','I^G_x','I^B_x'],
    'I^CFA_y': ['I^B_y','I^G_y','I^G_y','I^R_y']
}
cmaps = {
    'I^CFA': ['blue','red','green'],
    'S^R': ['red',[0.68,0.68,0.68]],
    'S^G': ['green',[0.68,0.68,0.68]],
    'S^B': ['blue',[0.68,0.68,0.68]],
    'S^G,R': ['green',[0.68,0.68,0.68]],
    'S^G,B': ['green',[0.68,0.68,0.68]],
    'I^CFA_x': ['grey'],
    'I^CFA_y': ['grey']
}

for what_to_draw, v in cmaps.items():
    #what_to_draw = 'I^CFA'
    # start drawing
    fig1, ax1 = plt.subplots()
    for tic in ax1.xaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = tic.label1On = False
        tic.label2On = True
    for tic in ax1.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    plt.xticks(range(0,image_data[what_to_draw][0].size))
    plt.tick_params(axis='both', which='major', pad=10, labelsize=18)
    plt.tick_params(axis='y', which='major', pad=15)
    draw_cfa(image_data[what_to_draw], 'labels[what_to_draw][2*(y%2)+x%2]')

    plt.imshow(image_data[what_to_draw], colors.ListedColormap(cmaps[what_to_draw]), interpolation='none')
    #plt.show()
    plt.savefig(what_to_draw+'.png', bbox_inches='tight')
