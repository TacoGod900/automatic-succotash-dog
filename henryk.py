import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

# Room dimensions
ROOM_SIZE = 20
CUBE_SIZE = 1


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def DrawRoom():
    """Draw a room made of lines"""
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    
    # Room is a box from -ROOM_SIZE to +ROOM_SIZE
    half = ROOM_SIZE
    
    # Bottom square
    glVertex3f(-half, -half, -half)
    glVertex3f(half, -half, -half)
    
    glVertex3f(half, -half, -half)
    glVertex3f(half, -half, half)
    
    glVertex3f(half, -half, half)
    glVertex3f(-half, -half, half)
    
    glVertex3f(-half, -half, half)
    glVertex3f(-half, -half, -half)
    
    # Top square
    glVertex3f(-half, half, -half)
    glVertex3f(half, half, -half)
    
    glVertex3f(half, half, -half)
    glVertex3f(half, half, half)
    
    glVertex3f(half, half, half)
    glVertex3f(-half, half, half)
    
    glVertex3f(-half, half, half)
    glVertex3f(-half, half, -half)
    
    # Vertical edges
    glVertex3f(-half, -half, -half)
    glVertex3f(-half, half, -half)
    
    glVertex3f(half, -half, -half)
    glVertex3f(half, half, -half)
    
    glVertex3f(half, -half, half)
    glVertex3f(half, half, half)
    
    glVertex3f(-half, -half, half)
    glVertex3f(-half, half, half)
    
    glEnd()
    glColor3f(1, 1, 1)


def clamp_cube_position(pos, limit):
    """Clamp cube position so it stays within room bounds"""
    return max(-limit + CUBE_SIZE, min(limit - CUBE_SIZE, pos))


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Set up projection matrix
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)

    # Camera position and rotation
    camera_x, camera_y, camera_z = 0, 5, 30
    camera_rotation_x, camera_rotation_y = -10, 0

    # Cube position
    cube_x, cube_y, cube_z = 0, 0, 0

    # Velocities
    camera_vel_x, camera_vel_y, camera_vel_z = 0, 0, 0
    camera_rot_vel_x, camera_rot_vel_y = 0, 0
    cube_vel_x, cube_vel_y, cube_vel_z = 0, 0, 0

    # Control speeds
    camera_speed = 0.3
    camera_rot_speed = 2
    cube_speed = 0.1
    zoom_level = 1.0

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            # Check for key down event
            if event.type == pygame.KEYDOWN:
                # Camera movement with IJKL
                if event.key == pygame.K_i:
                    camera_vel_z = -camera_speed
                if event.key == pygame.K_k:
                    camera_vel_z = camera_speed
                if event.key == pygame.K_j:
                    camera_vel_x = -camera_speed
                if event.key == pygame.K_l:
                    camera_vel_x = camera_speed

                # Camera rotation with GVBN
                if event.key == pygame.K_g:
                    camera_rot_vel_y = -camera_rot_speed
                if event.key == pygame.K_v:
                    camera_rot_vel_y = camera_rot_speed
                if event.key == pygame.K_b:
                    camera_rot_vel_x = camera_rot_speed
                if event.key == pygame.K_n:
                    camera_rot_vel_x = -camera_rot_speed

                # Cube movement with WASD
                if event.key == pygame.K_d:
                    cube_vel_x = cube_speed
                if event.key == pygame.K_a:
                    cube_vel_x = -cube_speed
                if event.key == pygame.K_w:
                    cube_vel_y = cube_speed
                if event.key == pygame.K_s:
                    cube_vel_y = -cube_speed

                # Zoom with +/-
                if event.key == pygame.K_EQUALS:
                    zoom_level *= 1.1
                if event.key == pygame.K_MINUS:
                    zoom_level /= 1.1

            # Check for key up event
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_i or event.key == pygame.K_k:
                    camera_vel_z = 0
                if event.key == pygame.K_j or event.key == pygame.K_l:
                    camera_vel_x = 0
                if event.key == pygame.K_g or event.key == pygame.K_v:
                    camera_rot_vel_y = 0
                if event.key == pygame.K_b or event.key == pygame.K_n:
                    camera_rot_vel_x = 0
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    cube_vel_x = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    cube_vel_y = 0

        # Update camera position
        camera_x += camera_vel_x
        camera_y += camera_vel_y
        camera_z += camera_vel_z

        # Update camera rotation
        camera_rotation_x += camera_rot_vel_x
        camera_rotation_y += camera_rot_vel_y

        # Update cube position with boundary checking
        cube_x = clamp_cube_position(cube_x + cube_vel_x, ROOM_SIZE)
        cube_y = clamp_cube_position(cube_y + cube_vel_y, ROOM_SIZE)
        cube_z = clamp_cube_position(cube_z + cube_vel_z, ROOM_SIZE)

        # Clear and setup view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        glTranslatef(0, 0, -30 * zoom_level)
        glRotatef(camera_rotation_x, 1, 0, 0)
        glRotatef(camera_rotation_y, 0, 1, 0)
        glTranslatef(-camera_x, -camera_y, -camera_z)

        # Draw room
        DrawRoom()

        # Draw cube at its position
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(cube_x, cube_y, cube_z)
        Cube()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)


main()
