import numpy as np
from rungekutta import R4K
from collections import deque
import pygame


l1 = 1
l2 = 1
m1 = 1
m2 = 1
g = 2*9.8

pendules_n = 10
step_size = 0.01 # Pour Runge-Kutta




def omega_1(t, th1, th2, omeg1, omeg2):
    return omeg1
def omega_2(t, th1, th2, omeg1, omeg2):
    return omeg2

def alpha_1(t, th1, th2, omeg1, omeg2):
    return (l1*m2*np.sin(2*th1 - 2*th2)*omeg1**2 + 2*l2*m2*np.sin(th1 - th2)*omeg2**2 + 2*g*m1*np.sin(th1) + g*m2*np.sin(th1 - 2*th2) + g*m2*np.sin(th1))/(l1*(-2*m1 + m2*np.cos(2*th1 - 2*th2) - m2))

def alpha_2(t, th1, th2, omeg1, omeg2):
    return (-2*l1*m1*np.sin(th1 - th2)*omeg1**2 - 2*l1*m2*np.sin(th1 - th2)*omeg1**2 - l2*m2*np.sin(2*th1 - 2*th2)*omeg2**2 - g*m1*np.sin(2*th1 - th2) + g*m1*np.sin(th2) - g*m2*np.sin(2*th1 - th2) + g*m2*np.sin(th2))/(l2*(-2*m1 + m2*np.cos(2*th1 - 2*th2) - m2))

r4ks = [R4K(0.01, omega_1, omega_2, alpha_1, alpha_2) for _ in range(pendules_n)]
for i, r  in enumerate(r4ks):
    r.set_init_vars(0, np.pi, np.pi/2-0.0001*i, 0, 0)



pygame.init()
screen = pygame.display.set_mode([800, 800])
running = True

pivot_pos_x = 400
pivot_pos_y = 400
rod_length = 70


points = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    for r4k in r4ks:
        n = r4k.step()
        thh1, thh2 = map(float, n[1:3])

        x1 = rod_length * l1 * np.sin(thh1)
        y1 = rod_length * -l1 * np.cos(thh1)
        x2 = x1 + rod_length * l2*np.sin(thh2)
        y2 = y1 - rod_length * l2*np.cos(thh2)

        points.append((x2, y2))

        points = points[-2000:]
        for p in points:
            pygame.draw.circle(screen, (0, 0, 0), (p[0]+pivot_pos_x, -p[1]+pivot_pos_y), 1)


        pygame.draw.line(screen, (255, 0, 0), (pivot_pos_x, pivot_pos_y), (x1+pivot_pos_x, -y1+pivot_pos_y), 3)
        pygame.draw.line(screen, (255, 0, 0), (x1+pivot_pos_x, -y1+pivot_pos_y), (x2+pivot_pos_x, -y2+pivot_pos_y), 3)
        pygame.draw.circle(screen, (0, 255, 0), (pivot_pos_x, pivot_pos_y), 6)
        pygame.draw.circle(screen, (0, 0, 255), (x1+pivot_pos_x, -y1+pivot_pos_y), 10)
        pygame.draw.circle(screen, (0, 0, 255), (x2+pivot_pos_x, -y2+pivot_pos_y), 10)

    pygame.display.flip()

pygame.quit()
