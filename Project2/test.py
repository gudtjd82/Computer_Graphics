import glm

t_x1 = (4 - 2)*2
t_x2 = (4-2)/20
T_spread = glm.translate((-t_x1, -t_x2,0))
Trans1 = glm.translate((3,7.12,0))
Trans2 = T_spread * glm.translate((3,7.17,0)) 
Trans3 = glm.translate((3-t_x1*2,7.22-t_x2*2,0)) 
Trans4 = glm.translate((3-t_x1*3,7.27-t_x2*3,0)) 

print((T_spread*2) * glm.translate((3,7.17,0)))
print("----------------------------------")
print(glm.translate((3-t_x1*2,7.22-t_x2*2,0)))