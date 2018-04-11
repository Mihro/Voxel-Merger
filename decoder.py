import struct
file = "test.vox"

class cuboid:
    def __init__(self, origin):
        self.x = origin[0]
        self.y = origin[1]
        self.z = origin[2]
        self.l = 1
        self.w = 1
        self.h = 1

def importVoxels(path):
    voxel_list = []  
    with open(path, 'rb') as f:
        bytes = f.read(4)
        file_id = struct.unpack("4s",  bytes)[0]
        if file_id != b'VOX ':
            print('Not a VOX file.')
        else:
            f.seek(32)
            dimensions = struct.unpack('iii',f.read(12))
            print("Model dimensions:",dimensions)
            f.seek(56)
            bytes = f.read(4)
            numvoxels = struct.unpack('i', bytes)[0]
            print("Reading", numvoxels, "voxels...")
            for x in range(0, numvoxels):
                bytes = f.read(4)
                voxel = struct.unpack('bbbb', bytes)
                voxel_list.append(voxel)
        voxel_list.sort(key=lambda v:(v[2],v[1],v[0]))
        print() 
    return dimensions, voxel_list

def pass_1D(dimensions,voxels):
    objects = []
    object_count = 0
    plane_coords = sorted(set([v[1:3] for v in voxels]),key=lambda c:(c[1],c[0]))
    for y,z in plane_coords:
        prev_x = None
        x_voxels = list(filter(lambda v: v[1]==y and v[2]==z, voxels))
        for i,x in enumerate([coord[0] for coord in x_voxels]):
            if x-1 != prev_x:
                new_origin = x_voxels[i]
                objects.append(cuboid(new_origin))
            else:
                
                objects[-1].l += 1
            prev_x = x
            
    print("1D Pass - Object Origins:")
    print("\t    Origin  Size")
    for i,o in enumerate(objects):
        print("Object"+" "*(1-(i+1)//10),i+1,"-",o.x,o.y,o.z," ",o.l,o.w,o.h)

    return objects

dimensions, voxels = importVoxels(file)
objects = pass_1D(dimensions, [v[:3] for v in voxels])


print("\nCompleted!")
