~VERSION INFORMATION
VERS.                       3.0 : CWLS LOG ASCII STANDARD -VERSION 3.0
WRAP.                        NO : ONE LINE PER DEPTH STEP
DLM .                     COMMA : DELIMITING CHARACTER BETWEEN DATA COLUMNS
# Acceptable delimiting characters: SPACE (default), TAB, OR COMMA.
~Well Information
#MNEM  .UNIT        DATA                  DESCRIPTION
#----- -----     ----------           -----------------
STRT  .M         1670.0000              : First Index Value
STOP  .M          713.2500              : Last Index Value
STEP  .M           -0.1250              : STEP
NULL  .            -999.25              : NULL VALUE
COMP  .     ANY OIL COMPANY INC.        : COMPANY
WELL  .     ANY ET AL 12-34-12-34       : WELL
FLD   .     WILDCAT                     : FIELD
LOC   .     12-34-12-34W5M              : LOCATION
PROV  .     ALBERTA                     : PROVINCE
SRVC  .     ANY LOGGING COMPANY INC.    : SERVICE COMPANY
DATE  .     13/12/1986                  : LOG DATE  {DD/MM/YYYY}
UWI   .     100123401234W500            : UNIQUE WELL ID
API   .     12345678                    : API NUMBER
LAT   .DEG                     34.56789 : Latitude  {DEG}
LONG.DEG                     -102.34567 : Longitude  {DEG}
UTM   . 1234587  3489875                 : UTM LOCATION
~CURVE INFORMATION
#MNEM.UNIT          API CODES        CURVE DESCRIPTION
#-----------      ---------       -------------------------
DEPT .M                           :  1  DEPTH
DT   .US/M         60 520 32 00   :  2  SONIC TRANSIT TIME
RHOB .K/M3         45 350 01 00   :  3  BULK DENSITY
NPHI .V/V          42 890 00 00   :  4  NEUTRON POROSITY
SFLU .OHMM         07 220 04 00   :  5  RXORESISTIVITY
SFLA .OHMM         07 222 01 00   :  6  SHALLOW RESISTIVITY
ILM  .OHMM         07 120 44 00   :  7  MEDIUM RESISTIVITY
ILD  .OHMM         07 120 46 00   :  8  DEEP RESISTIVITY
~PARAMETER INFORMATION
#MNEM .UNIT         VALUE          DESCRIPTION
#---- -----       ---------      ----------------------
MUD   .          GEL CHEM          :   MUD TYPE
BHT   .DEGC        35.5000         :   BOTTOMHOLE TEMPERATURE
BS    .MM         200.0000         :   BIT SIZE
FD    .K/M3      1000.0000         :   FLUID DENSITY
MATR  .          SAND              :   NEUTRON MATRIX
MDEN  .          2710.0000         :   LOGGING MATRIX DENSITY
RMF   .OHMM       0.2160           :   MUD FILTRATE RESISTIVITY
DFD   .K/M3      1525.0000         :   DRILL FLUID DENSITY
~OTHER
     Note: The logging tools became stuck at 625 metres
     causing the data between 625 metres and 615 metres to be invalid.
~ASCII | CURVE
1670.000  123.450 2550.000   0.450  123.450  123.450  110.200  105.600
1669.875  123.450 2550.000   0.450  123.450  123.450  110.200  105.600
1669.750  123.450 2550.000   0.450  123.450  123.450  110.200  105.600

~Inclinometry_Definition
MD. M                                   : Measured Depth        {F}
TVD. M                                  : True Vertical Depth   {F}
AZIM.DEG                                : Borehole Azimuth      {F}
DEVI.DEG                                : Borehole Deviation    {F}

~Inclinometry | Inclinometry_Definition
0.00,0.00,290.00,0.00
100.00,100.00,234.00,0.00
200.00,198.34,284.86,1.43
300.00,295.44,234.21,2.04
400.00,390.71,224.04,3.93
500.00,482.85,224.64,5.88
600.00,571.90,204.39,7.41

~Perforations_Definition
PERFT.M                                : Perforation Top Depth    {F}
PERFB.M                                : Perforation Bottom Depth {F}
PERFD.SHOTS/M                          : Shots per meter          {F}
PERFT.                                 : Charge Type              {S}

~Perforations | Perforations_Definition
545.50,550.60,12,BIG HOLE
551.20,554.90,12,BIG HOLE
575.00,595.00,12,BIG HOLE