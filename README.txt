"""This part is only for ITC determining"""
ITC - isomethral temperature coefficient.

This program aimed to make a full set of computings after each
test which is carried out after physical experiments after fuel
reloadings at operating reactors as well as after the initial 
core loading at the nuclear power units. 

This program allows to determine full set of parameters necessary,
such as temperature reactivity coefficient, maximum current value
allows, power reactivity coefficient, differential and integral 
efficiencies of CR groups, EP protection worth, etc. 

This program presents the changes of the parameters during the 
reaching of the critically, estimating the core symmetry, etc.

STEPS (for ITC):
1. Run the module "main.py".
2. Press the "Open file" button. 
3. select the file ITC.txt.
4. The head of this file will be presented. It is possible co confirm
via the lowest scrollbar that this file includes 250-260 parameters.
5. Thereafter the ITC button sould be chosen as this part allows to
make a computings related only to this parameter.
6. In the window opened we need to select the necessary parameters.
Firstly, the time should be chosen. It is possible to choose one of
"_29.03.2023" and "2 Time MCDS". Just press one on those buttons and
press "Obtain time" to confirm your choice.
Secondly, the reactivity should be chosen. It locates in the end of
this list (use scrollbar to switch this list down) as 251 and 252 
parameters. It is possible to select one of them or both - the average
values will be used. Press the "Obtain reactivity" button.
The third step is to choose the temperature. It comes in a variety of
points from 64 - 68, from 73 - 77. It is possible to select one of
them to determine the ITC, or the set - the average values will be
used. Press the "Obtain temperature" button.
7. Close this window. In the initial window press the "START" button.
8. The new window "tk" will open. This window consists of follow 
information:
    In the uper-left corner some parameters;
    In the down-left corner the temperature and reactivity curves during
    the process;
    In the right-upper corner there are four fields to the results
    (three for the three methods and one is the average values), and two
    fields with reactivity and temperature values used.
In the middle-up position there are two fields to enter the beta and
the DTC parameters. To run this code as a test it is recommended to use
these common values for beta (Effective Delayed Neutron Fraction) and 
DTC (Fuel temperature coefficient of reactivity, Doppler coefficient):
    beta = 0.655
    DTC = -2.75
Press "Obtain beta" and "Obtain DTC" buttons.
9. The prefinal stage is to choose the interval. To choose the left
boarder click to the picture in the correct position. To choose the 
right boarder click to the picture in the correct position. To run this
code as a test it is recommended to click at the follow positions:
    left boarder (left mouse button click) approximately at 9.03, 
slightly right from "29 09:00";
    right boarder (right mouse button click) approximately at 9.16, 
slightly right from "29 09:15".
Two dashed vertical red lines will appear. Tho fields with reactivity and
temperature values used will be filled.
10. Finally, press the "Compute ITC" button. The results from each
technique and the average values will be presented at the upper-right
corner.

The three techniques description. 
The information describes ITC.