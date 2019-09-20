// Create end caps for smaller boxes that will use cardboard, acrylic or other
// sheet material for the sides. 

//Box Width (mm)
box_width_x = 50;
//Box Depth (mm)
box_depth_y = 25.645;
// Box Height (mm) won't effect end caps but is used to give prefered 
// dimensions for sheet goods (and possible svg output)
box_height_z = 50;
// Thickness of bracket sides (mm)
bracket_thickness = 2;
// Thickness of sheet good slot (mm)
cardboard_thickness = 4;
// Sheet good slot depth (mm)
slotdepth = 4;

// limited user servicable parts below
bot_cube_width = (2 * bracket_thickness) + cardboard_thickness + slotdepth;
bot_cube_len_x = box_width_x;
bot_cube_len_y = box_depth_y;
bot_cube_height = bracket_thickness;

outside_cube_width = bracket_thickness;
outside_cube_len_x = box_width_x;
outside_cube_len_y = box_depth_y;
outside_cube_height = bracket_thickness + slotdepth;

inside_cube_width = bracket_thickness;
inside_cube_len_x = box_width_x - 2 * (bracket_thickness + cardboard_thickness);
inside_cube_len_y = box_depth_y  - 2 * (bracket_thickness + cardboard_thickness);
inside_cube_height = bracket_thickness + slotdepth;

module end_cap(xlt=[0,0,0]) {
    translate(xlt)
    union() {
        // Bottom
        cube([bot_cube_len_x, bot_cube_width, bot_cube_height]);

        rotate(a=90, v=[0,0,1])
        translate([0, -bot_cube_width, 0])
        cube([bot_cube_len_y, bot_cube_width, bot_cube_height]);

        translate([0, box_depth_y - bot_cube_width , 0])
        cube([bot_cube_len_x, bot_cube_width, bot_cube_height]);

        rotate(a=90, v=[0,0,1])
        translate([0, -(bot_cube_len_x), 0])
        cube([bot_cube_len_y, bot_cube_width, bot_cube_height]);

        // Outside
        cube([bot_cube_len_x, outside_cube_width, outside_cube_height]);

        rotate(a=90, v=[0,0,1])
        translate([0, -bracket_thickness, 0])
        cube([bot_cube_len_y, outside_cube_width, outside_cube_height]);

        translate([0, box_depth_y - bracket_thickness , 0])
        cube([bot_cube_len_x, outside_cube_width, outside_cube_height]);

        rotate(a=90, v=[0,0,1])
        translate([0, -(bot_cube_len_x), 0])
        cube([bot_cube_len_y, outside_cube_width, outside_cube_height]);

        // Inside
        translate([cardboard_thickness + bracket_thickness, cardboard_thickness + bracket_thickness, 0])
        cube([inside_cube_len_x, inside_cube_width, inside_cube_height]);

        rotate(a=90, v=[0,0,1])
        translate([cardboard_thickness + bracket_thickness, -(2*bracket_thickness+cardboard_thickness), 0])
        cube([inside_cube_len_y, inside_cube_width, inside_cube_height]);

        translate([cardboard_thickness + bracket_thickness, box_depth_y - (2*bracket_thickness) -       cardboard_thickness , 0])
        cube([inside_cube_len_x, inside_cube_width, inside_cube_height]);

        rotate(a=90, v=[0,0,1])
        translate([cardboard_thickness + bracket_thickness, -(bot_cube_len_x-cardboard_thickness-bracket_thickness), 0])
        cube([inside_cube_len_y, inside_cube_width, inside_cube_height]);
    }
}

 end_cap(xlt=[0,0,0]);
 end_cap(xlt=[0,box_depth_y + 2,0]);
