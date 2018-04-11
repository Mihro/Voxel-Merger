import struct
file = "test.vox"

def importVoxels(path):
    voxel_list = []  
    with open(path, 'rb') as f:
        bytes = f.read(4)
        file_id = struct.unpack("4s",  bytes)[0]
        if file_id != b'VOX ':
            print('Not a VOX file.')
        else:
            f.seek(32)
            size_x, size_y, size_z = struct.unpack('iii',f.read(12))
            dimensions = (size_x,size_y,size_z)
            print(dimensions)
            f.seek(56)
            bytes = f.read(4)
            numvoxels = struct.unpack('i', bytes)[0]
            print("Reading", numvoxels, "voxels...")
            for x in range(0, numvoxels):
                bytes = f.read(4)
                voxel = struct.unpack('bbbb', bytes)
                voxel_list.append(voxel)
        voxel_list.sort(key=lambda v:(v[2],v[1],v[0]))
            
    return dimensions, voxel_list

def pass_1D(dimensions,voxels):
    objects = []
    object_count = 0
    plane_coords = sorted(set([v[1:3] for v in voxels]))
    for y,z in plane_coords:
        prev_x = None
        x_voxels = list(filter(lambda v: v[1]==y and v[2]==z, voxels))
        for x in enumerate([coord[0] for coord in x_voxels]):
            if x[1]-1 != prev_x:
                objects.append(x_voxels[x[0]])
            prev_x = x[1]
            
    print("1D Object Origins:")
    for o in objects:
        print("\t",o)

dimensions, voxels = importVoxels(file)
pass_1D(dimensions, [v[:3] for v in voxels])


print("Completed!")
