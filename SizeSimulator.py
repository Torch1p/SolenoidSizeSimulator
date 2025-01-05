import femm
import math

filePath = 'C:/Users/matis/Documents/MakerPortfolio/Code'
results = []

# Given constants
lengthMAX = 26
turnsMAX = 1000
# changes in loop
turnsChange = 100
lengthChange = 2
# start constants
length = 12
# Constants
WireDia = 1
mosfet_resist = 0
BallDiameter = 15
gp = 17 + 1*2 # gap between solenoids (1mm is the wall of the track)

while length <= lengthMAX:
    turns = 200
    while turns <= turnsMAX:
        Rbase = gp / 2 # Base radius from the center to the inner edge of the coil
        n = math.floor(length / WireDia) # Number of turns that fit in one layer
        layers = math.ceil(turns / n) # Number of layers needed
        
        width = 0 # Total thickness of the coil starts at zero
        total_c = 0 # Total length of the wire
        turns_remaining = turns # Remaining turns to place in the coil

        # Loop through each layer, calculating the circumference and accumulating the total length
        while turns_remaining > 0:
            R = Rbase + width + WireDia / 2 # Radius at the center of the current layer
            turns_in_layer = min(n, turns_remaining) # Turns that fit in the current layer
            c = 2 * math.pi * R * turns_in_layer # Length of wire in the current layer
            total_c += c # Accumulate the total length
            width += WireDia # Increase the width for the next layer
            turns_remaining -= turns_in_layer # Subtract the turns placed in this layer

        # Calculate the total resistance
        Resist = (0.000021772 * total_c)
        volts = 12
        Amperes = volts / Resist



        # For the drawings
        gap = gp + width
        arc1 = width + gp/2 - BallDiameter/2 
        arc2 = width + gp/2 + BallDiameter/2
        sensorsFromSolenoids = -6

        femm.openfemm()

        #  set up
        femm.newdocument(0)
        femm.mi_probdef(0,"millimeters", "planar", 1e-008)
        femm.mi_addboundprop("Boundary",0,0,0,0,0,0,0,0,0,0,0)
        femm.mi_getmaterial("Air")
        femm.mi_getmaterial("N35")
        femm.mi_getmaterial("1mm")

        femm.mi_addcircprop("Coil", -Amperes, 1)

        # drawing the first coil (right - down - left  - up)
        femm.mi_drawline(0,0,width,0)
        femm.mi_drawline(width,0,width,length)
        femm.mi_drawline(width,length,0,length)
        femm.mi_drawline(0,length,0,0)

        # drawing the second coil
        femm.mi_drawline(gap,0 ,width+ gap,0)
        femm.mi_drawline(width + gap,0, width+gap,length)
        femm.mi_drawline(width + gap,length,gap ,length)
        femm.mi_drawline(gap,length,gap,0)

        # drawing the ball
        femm.mi_drawarc(arc1,sensorsFromSolenoids,arc2,sensorsFromSolenoids,180,1)
        femm.mi_drawarc(arc2,sensorsFromSolenoids ,arc1,sensorsFromSolenoids,180,1)

        # adding block labels
        femm.mi_addblocklabel(width/2, length/2)
        femm.mi_addblocklabel(gap+width/2, length/2)
        femm.mi_addblocklabel(width+gp/2, sensorsFromSolenoids)
        femm.mi_addblocklabel(width+gp/2, 10)

        # air
        femm.mi_selectlabel(width+gp/2, 10)
        femm.mi_setblockprop("Air",0,0,"",0,0,1)
        femm.mi_clearselected()

        # ball
        femm.mi_selectlabel(width+gp/2,sensorsFromSolenoids)
        femm.mi_setblockprop("N35",0,0,"",0,0,1)
        femm.mi_clearselected()

        # coil1
        femm.mi_selectlabel(width/2, length/2)
        femm.mi_setblockprop("1mm",0,0,"Coil",0,0,turns)
        femm.mi_clearselected()

        # coil2
        femm.mi_selectlabel(gap+width/2, length/2)
        femm.mi_setblockprop("1mm",0,0,"Coil",0,0,turns)
        femm.mi_clearselected()

        #boundry
        femm.mi_makeABC()

    
        femm.mi_saveas("C:/Users/matis/Documents/MakerPortfolio/Code/ZPDBEST.fem")
        femm.mi_analyze()
        femm.mi_loadsolution()

        femm.mo_selectblock(width+gp/2,sensorsFromSolenoids)
        force = femm.mo_blockintegral(19)

        results.append({"Force": round(force,7), "length": length, "Turns": turns, "AMPS": round(Amperes, 2)})
        #print("length", length, "Turns", turns, "Force", round(force,7))
        turns += turnsChange
          
    length = round(length + lengthChange, 2)
with open(filePath, 'a') as file:
    file.write('---------NEW DATA ENTRY----------\n')
    for result in results:
        file.write(f"Force: {result['Force']},  Turns: {result['Turns']}, Length: {result['length']}, Amps: {result['AMPS']}\n")
sorted_data = sorted(results, key=lambda x: x["Force"], reverse=True)
top_entries = sorted_data[:7]

for entry in top_entries:
    print(f"SORTED,Force: {entry['Force']}, Length: {entry['length']}, Turns: {entry['Turns']}, Amps: {entry['AMPS']}")
