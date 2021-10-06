import subprocess
import argparse
import cairo

# MacOS
OpenScad_Path = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"


# page dimensions in points (1 point = 1"/72 or 1 mm = 2.83465 points)
pg_x = 612
pg_y = 792

# Thickness of bracket sides (mm)
bracket_thickness = 2
# Thickness of sheet good slot (mm)
cardboard_thickness = 4
# Sheet good slot depth (mm)
slotdepth = 4

def run(cmd):
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
    )
    stdout, stderr = proc.communicate()
 
    return proc.returncode, stdout, stderr


def end_caps(width_x,depth_y,slotdepth=4,bracket_thickness=2,cardboard_thickness=4):
    # openscad -o output.stl -D 'model="input.stl"' test.scad

    cmd = [OpenScad_Path,'-o','output.stl',
    '-D', 'box_width_x={}'.format(width_x),
    '-D', 'box_depth_y={}'.format(depth_y),
    '-D', 'slotdepth={}'.format(slotdepth),
    '-D', 'bracket_thickness={}'.format(bracket_thickness),
    '-D', 'cardboard_thickness={}'.format(cardboard_thickness),
    'simplebox.scad']
    #print(cmd)

    return run(cmd)
    
    #print("out: '{}'".format(out))
    #print("err: '{}'".format(err))
    #print("exit: {}".format(code))

 
def parse_box_dimensions(arg_str, inches=False):
    '''Split the box dimensions and put find smallest dimensions first'''
    dims = arg_str.lower().split('x')
    if len(dims) < 3 or len(dims) >3:
        print("ERROR: Dimensions were either to small or to large",str(dims))
        exit()
    try:
        dims = [float(a) for a in dims]
    except:
        print("ERROR: Dimensions has values that aren't able to be converted to floats",str(dims))
        exit()
    else:
        dims.sort()
        if (inches):
            # convert to millimeter
            dims = [a * 25.4 for a in dims]
        #print(dims)
        return(dims)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Make a box. This will create the STLs and SVG required to build a box in a minimal 3D print fashion.')
    #parser.add_argument('--in', action='store_true',help='The dimension values are given in inches')
    parser.add_argument('--ct', type=float,help='Cardboard thickness')
    parser.add_argument('--sd', type=float,help='Slot Depth')
    parser.add_argument('--bt', type=float,help='Bracket Thickness')
    parser.add_argument('dimensions', type=str,
                        help='Dimensions in the form of widthxdepthxheight (i.e. 5.2x3.6x9.12)')
    
    args = parser.parse_args()
    
    dims = parse_box_dimensions(vars(args)['dimensions'],False)
    
    if 'ct' in vars(args) and vars(args)['ct'] is not None:
        cardboard_thickness = vars(args)['ct']
    if 'sd' in vars(args) and vars(args)['sd'] is not None:
        slotdepth = vars(args)['sd']
    if 'bt' in vars(args) and vars(args)['bt'] is not None:
        bracket_thickness = vars(args)['bt']
 
    # Call openSCAD to create STLs of the end caps. Stored in output.stl
    end_caps(dims[0],dims[1],slotdepth,bracket_thickness,cardboard_thickness)

    # Calculate top & bottom cut outs
    tb_x = dims[0] - ((4*bracket_thickness) + (2*cardboard_thickness))
    tb_y = dims[1] - ((4*bracket_thickness) + (2*cardboard_thickness))
    
    # Calculate sides 
    s_x = dims[0] - ((2*bracket_thickness) + (cardboard_thickness))
    s_y = dims[1] - ((2*bracket_thickness) + (cardboard_thickness))
    s_z = dims[2] - (2*bracket_thickness)
    # Total length of side on the x and y plane
    t_nz = (2*s_x) + (2*s_y)
    # Height in z direction
    t_z = s_z
    # convert to points
    ptb_x = tb_x * 2.83465
    ptb_y = tb_y * 2.83465
    ps_x  = s_x * 2.83465
    ps_y  = s_y * 2.83465
    ps_z  = s_z * 2.83465
    pt_nz = t_nz * 2.83465
    pt_z  = t_z * 2.83465
    
    # See if sides will fit on a 8.5" x 11" page
    if (pt_nz < (pg_x - 36)) and (pt_z < (pg_y -36)):
        # Side on paper start point
        sop_s_x = 18
        sop_s_y = 18
        # Side on paper width
        sop_w = pt_nz
        sop_h = pt_z
        # Bend lines
        bl_tby = sop_s_y
        bl_tey = sop_s_y + 18
        bl_bby = sop_s_y + sop_h
        bl_bey = bl_bby - 18
        bl_1_x = sop_s_x + ps_x
        bl_2_x = bl_1_x + ps_y
        bl_3_x = bl_2_x + ps_x
        s_dir_horz = True
    elif (pt_nz < (pg_y - 36)) and (pt_z < (pg_x - 36)):
        # Side on paper start point
        sop_s_x = 18
        sop_s_y = 18
        # Side on paper width
        sop_h = pt_nz
        sop_w = pt_z
        # Bend lines
        bl_tbx = sop_s_x
        bl_tex = sop_s_x + 18
        bl_bbx = sop_s_x + sop_w
        bl_bex = bl_bbx - 18
        bl_1_y = sop_s_y + ps_x
        bl_2_y = bl_1_y + ps_y
        bl_3_y = bl_2_y + ps_x
        s_dir_horz = False
    else:
        # won't fit on this size paper in either orientation
        print("ERROR: sides won't fit on this size paper in either orientation. Not creating SVG.")
        exit()

        
    # See how to print top and bottom
    if (2.01*ptb_x < pg_x - 36) and (ptb_y < pg_y - 36):
        rec_1 = [18,18,ptb_x,ptb_y]
        rec_2 = [(18 + 1.01 * ptb_x),18,ptb_x,ptb_y]
    elif (2.01*ptb_x < pg_y - 36) and (ptb_y < pg_x - 36):
        rec_1 = [18,18,ptb_y,ptb_x]
        rec_2 = [18,(18 + 1.01 * ptb_y),ptb_y,ptb_x]
    elif (ptb_x < pg_x - 36) and (2.01*ptb_y < pg_y - 36):
        rec_1 = [18,18,ptb_x,ptb_y]
        rec_2 = [18,(18 + 1.01 * ptb_x),ptb_x,ptb_y]
    elif (ptb_x < pg_y - 36) and (2.01*ptb_y < pg_x - 36):
        rec_1 = [18,18,ptb_y,ptb_x]
        rec_2 = [(18 + 1.01 * ptb_y),18,ptb_y,ptb_x]
    else:
        print("ERROR: top and bottom won't fit on this size paper in any orientation. Not creating SVG.")
        exit()
        
        
        
        
    ps = cairo.PDFSurface("pdffile.pdf", pg_x, pg_y)
    cr = cairo.Context(ps)
    # Side
    cr.rectangle(sop_s_x, sop_s_y, sop_w, sop_h)
    cr.set_source_rgb(0,0,0)
    cr.set_line_width(0.06)
    cr.stroke()
    # Bend lines
    if s_dir_horz:
        # Bend lines
        cr.move_to(bl_1_x, bl_tby)
        cr.line_to(bl_1_x, bl_tey)
        cr.move_to(bl_2_x, bl_tby)
        cr.line_to(bl_2_x, bl_tey)
        cr.move_to(bl_3_x, bl_tby)
        cr.line_to(bl_3_x, bl_tey)
        
        cr.move_to(bl_1_x, bl_bby)
        cr.line_to(bl_1_x, bl_bey)
        cr.move_to(bl_2_x, bl_bby)
        cr.line_to(bl_2_x, bl_bey)
        cr.move_to(bl_3_x, bl_bby)
        cr.line_to(bl_3_x, bl_bey)

        #cr.set_source_rgb(1, 0, 0)
        cr.set_line_width(0.06)
        cr.stroke()

    elif not s_dir_horz:
        # Bend lines        
        cr.move_to(bl_tbx, bl_1_y)
        cr.line_to(bl_tex, bl_1_y)
        cr.move_to(bl_tbx, bl_2_y)
        cr.line_to(bl_tex, bl_2_y)
        cr.move_to(bl_tbx, bl_3_y)
        cr.line_to(bl_tex, bl_3_y)
        
        cr.move_to(bl_bbx, bl_1_y)
        cr.line_to(bl_bex, bl_1_y)
        cr.move_to(bl_bbx, bl_2_y)
        cr.line_to(bl_bex, bl_2_y)
        cr.move_to(bl_bbx, bl_3_y)
        cr.line_to(bl_bex, bl_3_y)

        #cr.set_source_rgb(1, 0, 0)
        cr.set_line_width(0.06)
        cr.stroke()
    cr.show_page()

    cr.rectangle(*rec_1)
    cr.rectangle(*rec_2)
    cr.set_source_rgb(0,0,0)
    cr.set_line_width(0.06)
    cr.stroke()
    cr.show_page()
