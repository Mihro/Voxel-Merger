import struct
mypath = "move mob.vox"

def importVox(path):
    with open(path, 'rb') as f:
        bytes = f.read(4)
        file_id = struct.unpack("4s",  bytes)[0]
        if file_id == b'VOX ':
            print("Reading...")
            matlist = [];
            f.seek(56)
            bytes = f.read(4)
            numvoxels = struct.unpack('I', bytes)
            for x in range(0, numvoxels[0]):
                bytes = f.read(4)
                voxel = struct.unpack('bbbB', bytes)
                matid = voxel[3]
                print(voxel[0], voxel[1], voxel[2], matid)
        else:
            print('Not a VOX file.')
           
importVox(mypath)

print("Completed!")
