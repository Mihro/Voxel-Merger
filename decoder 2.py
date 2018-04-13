import struct, copy

file = "test.vox"

class Cuboid(object):
  def __init__(self, pos, size=None):
    self.pos = pos
    if size is None:
      self.size = [1, 1, 1]
    else:
      self.size = size

  def __repr__(self):
    return "{}-{}-{}:{}x{}x{}".format(*self.pos, *self.size)

  def sameShape(self, other):
    return self.size == other.size

  def canMerge(self, other):
    valid = 0
    for i in range(3):
      if self.size[i] == other.size[i] and self.pos[i] == other.pos[i]:
        valid += 1
      elif abs((self.pos[i] + self.size[i]) - other.pos[i]) == 0:
        valid += 3
    return valid == 5 # 1 + 1 + 3

  class MergeException(Exception):
    pass

  def merge(self, other):
    if not self.canMerge(other):
      raise MergeException("Error merging cuboids {} and {}".format(self, other))
    for i in range(3):
      if abs((self.pos[i] + self.size[i]) - other.pos[i]) == 0:
        axis = i
    axisLabels = ["x","y","z"]
    print("\tMerging "+axisLabels[axis]+":", self, other,end=" ")
    if self.pos[axis] < other.pos[axis]:
      result = Cuboid(self.pos, self.size)
      result.size[axis] += other.size[axis]
    else:
      print(self.pos,other.pos)
      result = Cuboid(other.pos, other.size)
      result.size[axis] += self.size[axis]
    print("INTO", result)
    return result

def make3dList(x, y, z, default):
  return [[[copy.deepcopy(default) for _ in range(z)] for _ in range(y)] for _ in range(x)]

def importVoxels(path):
  with open(path, 'rb') as f:
    byts = f.read(4)
    file_id = struct.unpack("4s",  byts)[0]
    if file_id != b'VOX ':
      raise UserWarning("Not a VOX file!")
    f.seek(32)
    dimensions = struct.unpack('iii', f.read(12))
    print("Model dimensions: ", dimensions)
    model = make3dList(*dimensions, None)
    f.seek(56)
    byts = f.read(4)
    numvoxels = struct.unpack('i', byts)[0]
    print("Reading", numvoxels, "voxels...")
    for _ in range(0, numvoxels):
      byts = f.read(4)
      voxel = struct.unpack('bbbb', byts)[:3]
      model[voxel[0]][voxel[1]][voxel[2]] = Cuboid(voxel)
    print("Completed.\n")
  return dimensions, model

def scan(dimensions, model):
    resetCuboid = Cuboid((128,128,128))
    for z in range(1):#dimensions[2]
        print("\nZ"+str(z),end="\n")
        for y in range(dimensions[1]):
            print("\nY"+str(y),end=" ")
            for x in range(dimensions[0]):
                print("X"+str(x),end="")
                print("Current:",model[x][y][z])
                if type(model[x][y][z]) is Cuboid:
                    if x == 0:
                        pass
                    elif type(model[x-1][y][z]) is not Cuboid:
                        pass
                    else:
                        print("\tHas prev:", model[x-1][y][z])
                        if model[x-1][y][z].canMerge(model[x][y][z]):
                            model[x-1][y][z] = model[x][y][z] = model[x-1][y][z].merge(model[x][y][z])
                            print("Row 1:",[model[x][0][0] for x in range(dimensions[0])],end="\n\n")                
                
    print("\nDone!")

dimensions, voxelList = importVoxels(file)
scan(dimensions, voxelList)
