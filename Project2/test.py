import glm

v = glm.vec3(1, 2, 3)
t = glm.translate((v.x, v.y, v.z))

print("V: \n", v)
print("t: \n", t)