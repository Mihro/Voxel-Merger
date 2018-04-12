import struct, copy

file = "test.vox"

class Cuboid(object):
  def __init__(self, pos, size=[1, 1, 1]):
    self.pos = pos
    self.size = size

  def __repr__(self):
    return "{} {} {}:{}x{}x{}".format(*self.pos, *self.size)

  def sameShape(self, other):
    return self.size == other.size

  def canMerge(self, other):
    valid = 0
    for i in range(3):
      if self.size[i] == other.size[i] and self.pos[i] == other.pos[i]:
        valid += 1
      elif abs(self.pos[i] - other.pos[i]) == 1:
        valid += 3
    return valid == 5 # 1 + 1 + 3

  class MergeException(Exception):
    pass

  def merge(self, other):
    if not canMerge(self, other):
      raise MergeException("Error merging cuboids {} and {}".format(self, other))
    for i in range(3):
      if abs(self.pos[i] - other.pos[i]) == 1:
        axis = i
    if self.pos[axis] < other.pos[axis]:
      result = Cuboid(self.pos, self.size)
      result.size[axis] += other.size[axis]
    else:
      result = Cuboid(other.pos, other.size)
      result.size[axis] += self.size[axis]
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
  return model

voxelList = importVoxels(file)
print(voxelList)
