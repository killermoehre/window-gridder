#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Author: Silvio Knizek <killermoehre@gmx.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# I would love if someone could open a some repository for this and continue
# development, since my python is not good enough. A python3 port with gobject
# would be cool, too.

import argparse
from gtk import gdk

PACKAGE = "window_grid"

def argument_parser():
    """
    The argument parser. Takes only one number from the cmd line in the range of
    1 to 9.
    """
    parser = argparse.ArgumentParser(description='Tile the current window.',
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument('position',
        metavar='N',
        type=int,
        help='''an integer describing the position according to a keyboard keypad
┌─────────┬─────────┐
│         ┊         │
│    7    8    9    │
│         ┊         │
├┈┈┈┈4┈┈┈┈┼┈┈┈┈6┈┈┈┈┤
│         ┊         │
│    1    2    3    │
│         ┊         │
└─────────┴─────────┘
5 is pseudo maximized''',
        choices = xrange(1, 10)
        )
    return parser.parse_args()

def get_workarea():
    """
    List with x-offset, y-offset, width and height in pixel of the first desktop
    workarea relative to the root window.
    TODO: take not the first, but the current desktop (right now, all
    desktops are the same size, so it doesn't bother me)
    """
    root_win = gdk.get_default_root_window()
    win_property = gdk.atom_intern("_NET_WORKAREA")
    wa_list = root_win.property_get(win_property)[2]
    return([wa_list[0],
            wa_list[1],
            wa_list[2],
            wa_list[3]])

def get_borders(window):
    """
    Returns the left, right, top and bottem border width in pixel from
    the specified window.
    """
    border_list = window.property_get(gdk.atom_intern("_NET_FRAME_EXTENTS"))[2]
    return([border_list[0],
            border_list[1],
            border_list[2],
            border_list[3]])

def main():
    """
    Main function. In memory of good old languages *snicker*
    """
    args = argument_parser()
    screen = gdk.screen_get_default()
    active_window = screen.get_active_window()
    active_window.unmaximize()
    workarea = get_workarea()
    borders = get_borders(active_window)
    place_dic = {"x" : 0, "y" : 0, "width" : 0, "height" : 0}
    position = args.position
    ### Define the x ###
    if position in [1, 2, 4, 5, 7, 8]:
        place_dic["x"] = int(workarea[0])
    else:
        place_dic["x"] = int(workarea[0] + round(float(workarea[2]) / 2.0))
    ### Define the y ###
    if position in [4, 5, 6, 7, 8, 9]:
        place_dic["y"] = int(workarea[1])
    else:
        place_dic["y"] = int(workarea[1] + round(float(workarea[3]) / 2.0))
    ### Define the width ###
    if position in [2, 5, 8]:
        place_dic["width"] = int(workarea[2] - (borders[0] + borders[1]))
    else:
        place_dic["width"] = int(round(float(workarea[2]) / 2.0) - (borders[0] + borders[1]))
    ### Define the height ###
    if position in [4, 5, 6]:
        place_dic["height"] = int(workarea[3] - (borders[2] + borders[3]))
    else:
        place_dic["height"] = int(round(float(workarea[3]) / 2.0) - (borders[2] + borders[3]))

    active_window.move_resize(place_dic["x"],
                              place_dic["y"],
                              place_dic["width"],
                              place_dic["height"])
    active_window.get_geometry()
    gdk.exit((0))

if __name__ == '__main__':
    main()
