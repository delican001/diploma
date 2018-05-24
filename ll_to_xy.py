import math
RADIANS = 57.2957795

def DEG_TO_RADIANS(x):
    return (x / RADIANS)

def METERS_DEGLON(x):
    d2r = DEG_TO_RADIANS(x)
    return ((111415.13 * math.cos(d2r)) - (94.55 * math.cos(3.0 * d2r)) + (0.12 * math.cos(5.0 * d2r)))

def METERS_DEGLAT(x):
    d2r = DEG_TO_RADIANS(x)
    return (111132.09 - (566.05 * math.cos(2.0 * d2r)) + (1.20 * math.cos(4.0 * d2r)) - (0.002 * math.cos(6.0 * d2r)))

def lat_long_to_xy(source_lat, source_lon, origin_lat, origin_lon):
    y = (source_lon - origin_lon) * METERS_DEGLON(origin_lat)
    x = (source_lat - origin_lat) * METERS_DEGLAT(origin_lat)
    r = math.sqrt(x * x + y * y)
    ct = x / r
    st = y / r
    rotation_angle_degs = 0
    angle = DEG_TO_RADIANS(rotation_angle_degs)
    x = r * ((ct * math.cos(angle)) + (st * math.sin(angle)))
    y = r * ((st * math.cos(angle)) - (ct * math.sin(angle)))
    #xoffset_mtrs = 0
    #yoffset_mtrs = 0
    #pxpos_mtrs = x + xoffset_mtrs
    #pypos_mtrs = y + yoffset_mtrs
    return [x, y]
