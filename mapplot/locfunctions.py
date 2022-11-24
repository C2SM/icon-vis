####################################################################
## CLASS DEFINITION ##
# 1) area coordinates for hor cross
class Area_coordinates:
    # need 2 locations to delimit area
    name = 'AREANAME'
    latmin = 0
    lonmin = 0
    latmax = 0
    lonmax = 0
    locmarks = []

# 2) local coordinates for points
class Point_coordinates:
    def __init__(self, name, color, marker, lat, lon):
        self.name = name
        self.color = color
        self.marker = marker
        self.lat = lat
        self.lon = lon

####################################################################
## COORDINATE SET ##
# 1) local coordinates for points
# 1) a) Innsbruck
inn = Point_coordinates('Innsbruck', 'k','.',47.26,11.42)
# Salzburg
sal = Point_coordinates('Salzburg', 'k','.', 47.79,13.09)
# München
mun = Point_coordinates('Munich','k','.',48.14,11.57)
# Bozen
bz = Point_coordinates('Bozen','k','.', 46.49,11.36)
# Verona
ver = Point_coordinates('Verona', 'k','.',45.43,10.99)
# Venice
ven = Point_coordinates('Venice','k','.',45.33,12.27)

## meteo stations
# iun
iun = Point_coordinates('stat Universität','violet',"$u$",47.2642889,11.3861614)
# ifl
ifl = Point_coordinates('Station Flughafen','violet',"$f$",47.25846,11.3521825)

## ibox stations
# Hoch
hoch = Point_coordinates('ibox Hochhaueser','violet',"$h$",47.28755, 11.63122)
# Kols
kols = Point_coordinates('Kolsass','violet',"$k$",47.305, 11.622)
# Eggen
egg = Point_coordinates('ibox Eggen','violet',"$e$",47.3165,11.6162)
# Weer
weer = Point_coordinates('ibox Weerberg','violet',"$w$",47.299,11.672)
# Terf
terf = Point_coordinates('ibox Terfens','violet',"$t$", 47.325538,11.65247)
# Arb
arb = Point_coordinates('ibox Arbeser','violet',"$a$",47.320654,11.746592)

# 2) area coordinates for hor cross
# 2)a) icon domain
icon_domain = Area_coordinates()
icon_domain.name = 'icon_domain'
icon_domain.latmin = 42.7
icon_domain.lonmin = 1
icon_domain.latmax = 49.7
icon_domain.lonmax = 16.3
icon_domain.locmarks = []
icon_domain.locmarks.extend([inn,mun,ven])


# 2)b) eastern alps
eastern_alps = Area_coordinates()
eastern_alps.name = 'eastern_alps'
eastern_alps.latmin = 45
eastern_alps.lonmin = 9
eastern_alps.latmax = 49
eastern_alps.lonmax = 15
eastern_alps.locmarks = []
eastern_alps.locmarks.extend([inn,mun,ven,sal,bz,ver])

# 2)c) innsbruck area
inn_area = Area_coordinates()
inn_area.name = 'inn_area'
inn_area.latmin = 46.5
inn_area.lonmin = 10
inn_area.latmax = 48
inn_area.lonmax = 13
inn_area.locmarks = []
inn_area.locmarks.extend([inn, hoch, kols, weer, egg, weer, terf, arb, iun, ifl])

# 2)c) local area
local_area = Area_coordinates()
local_area.name = 'local_area'
local_area.latmin = 47.1
local_area.lonmin = 11.3
local_area.latmax = 47.5
local_area.lonmax = 11.8
local_area.locmarks = []
local_area.locmarks.extend([hoch, kols, weer, egg, weer, terf, arb, iun, ifl])

# 2)c) domain visualisation
domain_vis = Area_coordinates()
domain_vis.name = 'domain_vis'
domain_vis.latmin = 40
domain_vis.lonmin = 0
domain_vis.latmax = 50
domain_vis.lonmax = 20
domain_vis.locmarks = []
domain_vis.locmarks.extend([inn])

# 2)c) super zoom ifl
zoom = Area_coordinates()
zoom.name = 'zoom'
zoom.latmin = 47.2
zoom.lonmin = 11.2
zoom.latmax = 47.4
zoom.lonmax = 11.5
zoom.locmarks = []
zoom.locmarks.extend([ifl])


####################################################################
## COORDINATE SET ##
# print(eastern_alps.locmarks)
# for mark in eastern_alps.locmarks:
#     print(mark.name)