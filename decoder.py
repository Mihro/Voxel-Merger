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
                voxel = struct.unpack('bbbB', bytes)
                voxel_list.append(voxel)
        voxel_list.sort(key=lambda v:(v[2],v[1],v[0]))
            
    return dimensions, voxel_list

dimensions, voxels = importVoxels(file)

print("Completed!")
