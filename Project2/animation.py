import glm
from draw import draw_node
import numpy as np
from glfw.GLFW import *

#table:node, cards:node array, 
def animation_cardSpread(unif_locs, unif_vaos, unif_nodes, unif_objs, cards, VP, pos, th):
    # set local transformation of each node
    # spread and gather two cards - cards[0], cards[2]
    
    Trans1 = glm.translate(pos) * glm.translate((-th*1.7,0,0)) * glm.rotate(th, (0,1,0)) * glm.translate((0,0,-1))
    Trans2 = glm.translate((pos.x,pos.y+0.06,pos.z)) * glm.translate((th*1.7,0,0)) * glm.rotate(-th, (0,1,0)) * glm.translate((0,0,-1))
    # set transforms to cards 
    unif_nodes[cards[0]].set_transform(Trans1)
    unif_nodes[cards[1]].set_transform(glm.translate((pos.x,pos.y-0.06,pos.z-1-abs(th*2))))
    unif_nodes[cards[2]].set_transform(Trans2)
    unif_nodes["table"].update_tree_global_transform()
    # draw Cards
    for i in range(3):
        draw_node(unif_vaos[cards[i]], unif_nodes[cards[i]], VP, unif_locs["MVP"], unif_locs["color"], unif_objs[cards[i]])

def animation_chipShuffle(unif_locs, unif_vaos, unif_nodes, unif_objs, chip, VP, m, start_time, unit, x_pos, th, d):
    for i in range(5):
        if m < unit:    # top: 왼쪽 아래 이동, 반시계방향 회전
            # transforamtion variables
            t_x = 2*m*d
            t_y = m*0.75
            r = m*50*d
            T_xy = glm.translate((-t_x, -t_y,0))
            R = glm.rotate(np.radians(r), (0,0,1))

            # bottom chips
            # transfromation
            Trans_bot = glm.translate((x_pos,0.09*i,th*2+1))
            unif_nodes[chip].set_transform(Trans_bot)
            unif_nodes["table"].update_tree_global_transform()
            # draw bottom chips
            draw_node(unif_vaos["chip"], unif_nodes[chip], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["chip"])

            # top chips
            # transfromation
            Trans_top = T_xy * glm.translate((x_pos,0.09*i+0.45,th*2+1))* R
            unif_nodes[chip].set_transform(Trans_top)
            
        elif m < unit*2:    # top: 시계 방향 회전
            # transforamtion variables
            t_x = 2*unit*d
            t_y = unit*0.75
            r = unit*50-(m-unit)*50
            r *= d
            T_xy = glm.translate((-t_x, -t_y,0))
            R = glm.rotate(np.radians(r), (0,0,1))

            # bottom chips
            # transfromation
            Trans_bot = glm.translate((x_pos,0.09*i,th*2+1))
            unif_nodes[chip].set_transform(Trans_bot)
            unif_nodes["table"].update_tree_global_transform()
            # draw bottom chips
            draw_node(unif_vaos["chip"], unif_nodes[chip], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["chip"])

            # top chips
            # transfromation
            Trans_top = T_xy * glm.translate((x_pos,0.09*i+0.45,th*2+1)) * R
            unif_nodes[chip].set_transform(Trans_top)
            
        elif m < unit*3:    # top: 반시계 방향 회전
                            # bottom: 시계 방향 회전
            # transforamtion variables
            t_x = 2*unit*d
            t_y = unit*0.75
            r = (m-2*unit)*50*i/5
            r *= d
            T_xy = glm.translate((-t_x, -t_y,0))
            R_top = glm.rotate(np.radians(r), (0,0,1))
            R_bot = glm.rotate(np.radians(-r), (0,0,1))
            # bottom chips
            # transfromation
            Trans_bot = glm.translate((x_pos,0.09*i,th*2+1)) * R_bot
            unif_nodes[chip].set_transform(Trans_bot)
            unif_nodes["table"].update_tree_global_transform()
            # draw bottom chips
            draw_node(unif_vaos["chip"], unif_nodes[chip], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["chip"])

            # top chips
            # transfromation
            Trans_top = T_xy * glm.translate((x_pos,0.09*i+0.45,th*2+1)) * R_top
            unif_nodes[chip].set_transform(Trans_top)

        elif m < unit*4:        # top: 오른쪽 이동, 시계 방향 회전
                                # bottom: 반시계 방향 회전
            # transforamtion variables
            t_x = -2*unit + 2*(m-3*unit)
            t_x *= d
            t_y_top = -0.45 + (m-3*unit)*0.15*(i+1)
            t_y_bottom = (m-3*unit)*0.15*i
            r_old = unit*50*i/5
            r = r_old - (m-3*unit)*50*i/5
            r *= d
            T_top = glm.translate((t_x, t_y_top, 0))
            T_bot = glm.translate((0, t_y_bottom, 0))
            R_top = glm.rotate(np.radians(r), (0,0,1))
            R_bot = glm.rotate(np.radians(-r), (0,0,1))
            
            # bottom chips
            # transfromation
            Trans_bot = T_bot * glm.translate((x_pos,0.09*i,th*2+1)) * R_bot
            unif_nodes[chip].set_transform(Trans_bot)
            unif_nodes["table"].update_tree_global_transform()
            # draw bottom chips
            draw_node(unif_vaos["chip"], unif_nodes[chip], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["chip"])

            # top chips
            # transfromation
            Trans_top = T_top * glm.translate((x_pos,0.09*i+0.45,th*2+1)) * R_top
            unif_nodes[chip].set_transform(Trans_top)

        elif m < unit*5:                    # 유지
            # transforamtion variables
            t_y_bottom = unit*0.15*i
            t_y_top = unit*0.15*(i+1)-0.45
            T_bot = glm.translate((0, t_y_bottom, 0 ))
            T_top = glm.translate((0, t_y_top, 0 ))

            # bottom chips
            # transfromation
            Trans_bot = T_bot * glm.translate((x_pos,0.09*i,th*2+1))
            unif_nodes[chip].set_transform(Trans_bot)
            unif_nodes["table"].update_tree_global_transform()
            # draw bottom chips
            draw_node(unif_vaos["chip"], unif_nodes[chip], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["chip"])

            # top chips
            # transfromation
            Trans_top = T_top * glm.translate((x_pos,0.09*i+0.45,th*2+1))
            unif_nodes[chip].set_transform(Trans_top)

        else:                           # 초기화
            start_time = glfwGetTime()
        
        # draw top chips
        unif_nodes["table"].update_tree_global_transform()
        draw_node(unif_vaos["chip"], unif_nodes[chip], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["chip"])
    return start_time

def animation_showDown(unif_locs, unif_vaos, unif_nodes, unif_objs, VP, m, start_time, unit, ST):
    R = glm.rotate(np.radians(-20), (0,0,1))
    
    Trans1 = glm.translate((3,7.12,0)) * R * ST
    Trans2 = glm.translate((3,7.17,0)) * R * ST
    Trans3 = glm.translate((3,7.22,0)) * R * ST
    Trans4 = glm.translate((3,7.27,0)) * R * ST 

    for i in range(1):
        if m < unit:
            R = glm.rotate(np.radians(-20+40*m), (0,0,1))
            Trans1 = glm.translate((3,7.12,0)) * R * ST
            Trans2 = glm.translate((3,7.17,0)) * R * ST
            Trans3 = glm.translate((3,7.22,0)) * R * ST
            Trans4 = glm.translate((3,7.27,0)) * R * ST
        elif m < 3*unit:
            t_x1 = (m-unit)*2
            t_x2 = (m-unit)/20
            T_spread = glm.translate((-t_x1, -t_x2,0))
            Trans1 = glm.translate((3,7.12,0)) * ST
            Trans2 = T_spread * glm.translate((3,7.17,0)) * ST
            Trans3 = T_spread * T_spread *glm.translate((3,7.22,0)) * ST
            Trans4 = T_spread *T_spread *T_spread *glm.translate((3,7.27,0)) * ST
        elif m < 4*unit:
            t_x1 = 4*unit
            t_x2 = unit/10
            T_spread = glm.translate((-t_x1, -t_x2,0))
            Trans1 = glm.translate((3,7.12,0)) * ST
            Trans2 = T_spread * glm.translate((3,7.17,0)) * ST
            Trans3 = T_spread * T_spread *glm.translate((3,7.22,0)) * ST
            Trans4 = T_spread *T_spread *T_spread *glm.translate((3,7.27,0)) * ST
        elif m < 6*unit:
            t_x1 = 4*unit
            t_x2 = unit/10
            t_x3 = (m-unit*4)*2
            t_x4 = (m-unit*4)/20
            T_gather = glm.translate((-t_x1+t_x3, -t_x2+t_x4,0))
            Trans1 = glm.translate((3,7.12,0)) * ST
            Trans1 = glm.translate((3,7.12,0)) * ST
            Trans2 = T_gather * glm.translate((3,7.17,0)) * ST
            Trans3 = T_gather * T_gather *glm.translate((3,7.22,0)) * ST
            Trans4 = T_gather *T_gather *T_gather *glm.translate((3,7.27,0)) * ST
        elif m < 7*unit:
            R = glm.rotate(np.radians(-40*(m-unit*6)), (0,0,1))
            Trans1 = glm.translate((3,7.12,0)) * R * ST
            Trans2 = glm.translate((3,7.17,0)) * R * ST
            Trans3 = glm.translate((3,7.22,0)) * R * ST
            Trans4 = glm.translate((3,7.27,0)) * R * ST 
        elif m < 8*unit:
            R = glm.rotate(np.radians(-20), (0,0,1))
            Trans1 = glm.translate((3,7.12,0)) * R * ST
            Trans2 = glm.translate((3,7.17,0)) * R * ST
            Trans3 = glm.translate((3,7.22,0)) * R * ST
            Trans4 = glm.translate((3,7.27,0)) * R * ST 
        else:
            start_time = glfwGetTime()   

    # set transformation to cards
    unif_nodes["spade"].set_transform(Trans1)
    unif_nodes["dia"].set_transform(Trans2)
    unif_nodes["heart"].set_transform(Trans3)
    unif_nodes["clover"].set_transform(Trans4)
    unif_nodes["table"].update_tree_global_transform()
    # draw cards
    draw_node(unif_vaos["spade"], unif_nodes["spade"], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["spade"])
    draw_node(unif_vaos["dia"], unif_nodes["dia"], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["dia"])
    draw_node(unif_vaos["heart"], unif_nodes["heart"], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["heart"])
    draw_node(unif_vaos["clover"], unif_nodes["clover"], VP, unif_locs["MVP"], unif_locs["color"], unif_objs["clover"])

    return start_time
