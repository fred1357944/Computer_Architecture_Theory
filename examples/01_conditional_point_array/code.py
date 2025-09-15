import rhinoscriptsyntax as rs

pts = []

for i in range(x):
    if i < y:
        pt = rs.AddPoint(i,0,0)
        pts.append(pt)
    else:
        pt = rs.AddPoint(i,10,0)
        pts.append(pt)

pts_out = pts