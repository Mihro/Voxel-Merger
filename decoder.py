import struct
file = "test.vox"

class Cuboid:
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
    plane_coords = sorted(set([v[1:3] for v in voxels]),key=lambda c:(c[1],c[0]))
    for y,z in plane_coords:
        prev_x = None
        x_voxels = list(filter(lambda v: v[1]==y and v[2]==z, voxels))
        for i,x in enumerate([coords[0] for coords in x_voxels]):
            if x-1 != prev_x:
                new_origin = x_voxels[i]
                objects.append(Cuboid(new_origin))
            else:
                
                objects[-1].l += 1
            prev_x = x
            
    print("1D Pass - Object Origins:")
    print("\t    Origin  Size")
    for i,o in enumerate(objects):
        print("Object"+" "*(1-(i+1)//10),i+1,"-",o.x,o.y,o.z," ",o.l,o.w,o.h)
    print()
    return objects

def pass_2D(dimensions,objects):
    plane_coords = sorted(set([(o.x,o.z) for o in objects]))
    for x,z in plane_coords:
        prev_object = Cuboid((None,None,None))
        separate_object = Cuboid((None,None,None))
        y_objects = list(filter(lambda o: o.x==x and o.z==z, objects))
        print([(o.x,o.y,o.z) for o in y_objects])
        for i,o in enumerate([o for o in y_objects]):
            print((o.x,o.y,o.z))
            if (o.y-1,o.l,o.h) == (prev_object.y,prev_object.l,prev_object.h):
                print("Merge with",(separate_object.x,separate_object.y,separate_object.z))
                #Delete current object
            else:
                separate_object = o
                print("Separate Object")
            prev_object = o
        print()
                

dimensions, voxels = importVoxels(file)
objects = pass_1D(dimensions, [v[:3] for v in voxels])
pass_2D(dimensions,objects)

print("\nCompleted!")
