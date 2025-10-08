

"""
I would like you to implement key-store that supports versions.  For this problem, every item
should also have an integer version that increases every time the value associated with a key is
updated. All versions of the key should be accessible to a client -- you should be able to get not
only the latest version of a value but also a past version.

This store should implement the following API:
```
put(k, v) => returns version
get(k) => returns value for latest version
get(k, version) => returns value at that version
create(k, v) => returns version; errors if object already exists
put(k, v, expected_previous_version) => returns version; errors if existing version mismatch
```
"""


"""
  every item has a version number 
  all versions of key is accessible by client
"""
from collections import defaultdict

class VersionItem:
    def __init__(self):
        self.version = 0
        self.data = {}

    def put(self, value):
        self.version += 1
        self.data[self.version] = value

    def get(self, version = -1):
        if version == -1:
            version = self.version

        if version in self.data:
            return self.data[self.version]

        raise Exception(f"Invalid version {version}")
        

class KeyStore:
    def __init__(self):
        self.data = defaultdict(list)

    def put(self, k, v):
        self.data[k].append(v)

    def get(self, k, version = -1):
        if k not in self.data:
            raise Exception(f"key does not exist {k}")

        if version >= len(self.data[k]):
            raise Exception(f"Version does not exist {version}")

        if version == -1:
            return self.data[k][-1]
        else:
            return self.data[k][version]

    def create(self, k, v):
        """
         => returns version; errors if object already exists
        """
        if k in self.data:
            raise Exception(f"object already exists {k} {v}")

        # add version 
        self.data[k].append(v)
        return len(self.data[k]) - 1

    def put(self, k, v, expected_previous_version):
        """
          => returns version; errors if existing version mismatch
            expected_previous_version is the end
        """

        values = self.data[k]
        length = len(values)

        actual_previous_version = length - 1
        if actual_previous_version != expected_previous_version:
            raise Exception(f"existing version mismatch {k} {v} {expected_previous_version} {actual_previous_version}")

        values.append(v)
        return len(values) - 1


ks = KeyStore()
"""
ks.put("abc", 100)  # => returns version
result = ks.get("abc")
print(f"getting key abc: {result}")       #  => returns value for latest version

result = ks.get("abc", 0)
print(f"getting key abc, version 0: {result}")       #  => returns value for latest version

result = ks.get("abc", 1)
print(f"getting key abc, version 1: {result}")       #  => returns value for latest version

result = ks.get("abc", 2)    #  => should raise exception
print(f"getting key abc, version 2: {result}")       #  => returns value for latest version
"""

result = ks.create("cde", 3)    
print(f"create result {result}")

try:
    result = ks.create("cde", 3)   # should raise exception 
except Exception as e:
    print(e)

try:
    result = ks.put("cde", 5, 3)    #  => should raise exception
except Exception as e:
    print(e)
    
result = ks.put("cde", 5, 0)    
print(f"put result {result}")

