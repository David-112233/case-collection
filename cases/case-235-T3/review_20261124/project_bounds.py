"""Project the GT models' vertices with the GT's fixed camera, without a browser.

    python project_bounds.py <dir with the 11 .glb files>

The .glb files are the ones ground_truth.html loads (same commit a50f650 of ricardoolivaalonso/ThreeJS-Room14;
the same files are also served by raw.githubusercontent.com). Prints world-space bounds and the screen box of
each mesh for a few viewports: camera = (18, 6, 18) scaled to length 16, looking at the origin, vertical FOV 15.
Model offsets are the position.sub(...) values in ground_truth.html.
"""
import json,struct,sys,math
import numpy as np
def load(p):
    b=open(p,'rb').read(); l=struct.unpack('<I',b[12:16])[0]
    j=json.loads(b[20:20+l]); off=20+l; bl=struct.unpack('<I',b[off:off+4])[0]; bin_=b[off+8:off+8+bl]
    return j,bin_
def quat(q):
    x,y,z,w=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def pts(p,offset=(0,0,0)):
    j,bn=load(p); out={}
    for n in j['nodes']:
        if 'mesh' not in n: continue
        M=np.eye(4)
        if 'matrix' in n: M=np.array(n['matrix']).reshape(4,4).T
        else:
            S=np.diag(n.get('scale',[1,1,1])); R=quat(n.get('rotation',[0,0,0,1])); T=n.get('translation',[0,0,0])
            M[:3,:3]=R@S; M[:3,3]=T
        P=[]
        for pr in j['meshes'][n['mesh']]['primitives']:
            a=j['accessors'][pr['attributes']['POSITION']]; bv=j['bufferViews'][a['bufferView']]
            st=bv.get('byteOffset',0)+a.get('byteOffset',0)
            arr=np.frombuffer(bn,dtype='<f4',count=a['count']*3,offset=st).reshape(-1,3) if bv.get('byteStride',12)==12 else None
            P.append(arr)
        P=np.vstack(P); P=(M[:3,:3]@P.T).T+M[:3,3]+np.array(offset)
        out[n['name']]=P
    return out
cam=np.array([18,6,18.]); cam=cam/np.linalg.norm(cam)*16
f=-cam/np.linalg.norm(cam); r=np.cross(f,[0,1,0]); r/=np.linalg.norm(r); u=np.cross(r,f)
def project(P,W,H):
    d=P-cam; x=d@r; y=d@u; z=d@f
    t=math.tan(math.radians(7.5))
    ndcx=x/z/(t*W/H); ndcy=y/z/t
    return (ndcx+1)/2*W, (1-ndcy)/2*H
import os; DIR=sys.argv[1]
objs=pts(os.path.join(DIR,'room.glb'))
offs={'lampara':(-1.25,1.1,-.25),'robot':(-.25,-.42,-1.25),'sillon':(1.475,-1.125,.78),'lamparaBase':(-1.675,-.5,-1.25),'book':(-1.03,-.53,-1.23),'silla':(-.785,-.95,-.225),'jarron01':(.7,.15,-1.2),'jarron02':(-1.5,.77,-1.1),'jarron03':(-1.75,.77,-1.1),'pantalla':(0,0,0)}
for k,o in offs.items():
    for n,P in pts(os.path.join(DIR,f'{k}.glb'),o).items(): objs[k+':'+n]=P
allp=np.vstack(list(objs.values()))
print('world bounds',allp.min(0).round(2),allp.max(0).round(2), 'cam',cam.round(3))
for W,H in [(1280,800),(1920,1080),(375,812),(1838,1480),(1838,1440)]:
    X,Y=project(allp,W,H); print(W,H,'bbox x',round(X.min()),round(X.max()),'y',round(Y.min()),round(Y.max()))
W,H=1280,800
for k,P in objs.items():
    if k.startswith(('Text','Cube.0','Cube')) and ':' not in k: continue
    X,Y=project(P,W,H); c=P.mean(0)
    print(f'{k:28s} world_c {c.round(2)} ext {(P.max(0)-P.min(0)).round(2)}  screen x {X.min():.0f}-{X.max():.0f} y {Y.min():.0f}-{Y.max():.0f}')
