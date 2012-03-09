#! /usr/bin/python

# 
#  monitor.py
#  plate-detection
#  
#  Created by Jay Roberts on 2012-01-25.
#  Copyright 2012 GloryFish.org. All rights reserved.
# 

import sys
import cv
import pygame

class Monitor:
"""Detects circular shapes in images captured form a webcam. Provides a set of images used in the
   capture process for display. Also provides a list of the position and size of detetced circles"""    

    def __init__(self):
        self.threshhold = 200
        self.images = dict()
        self.camera = cv.CaptureFromCAM(-1)
        self.circles = []
    
    def get_image(self, image_name):
        """Converts the named image from the OpenCV format to one usable by PyGame"""
        image = self.images[image_name]
        
        source_image = cv.CreateMat(self.images[image_name].height, self.images[image_name].width, cv.CV_8UC3)
        if image_name == 'gray' or image_name == 'edges':
            cv.CvtColor(image, source_image, cv.CV_GRAY2RGB)
        else:        
            cv.CvtColor(image, source_image, cv.CV_BGR2RGB)

        return pygame.image.frombuffer(source_image.tostring(), cv.GetSize(source_image), "RGB")
    
    def capture(self):
        """Capture a frame from the camera, perform the Hough tranform and store the results."""
        self.images['original'] = cv.QueryFrame(self.camera)
        
        self.images['output'] = cv.CloneImage(self.images['original'])
        self.images['gray'] = cv.CreateImage(cv.GetSize(self.images['original']), cv.IPL_DEPTH_8U, 1)
        self.images['edges'] = cv.CreateImage(cv.GetSize(self.images['original']), cv.IPL_DEPTH_8U, 1)
    
        # Create a grayscale version
        cv.CvtColor(self.images['original'], self.images['gray'], cv.CV_BGR2GRAY)

    
        # Create an edge-detected version
        cv.Canny(self.images['gray'], self.images['edges'], self.threshhold, self.threshhold / 2, 3)

        hough_results = cv.CreateMat(640, 1, cv.CV_32FC3)
        
        cv.HoughCircles(self.images['gray'], hough_results, cv.CV_HOUGH_GRADIENT, 2, self.images['gray'].width / 18, self.threshhold, 300, 0, 0)

        self.circles = []
        
        for i in range(hough_results.rows):
            val = hough_results[i, 0]
            center = (int(val[0]), int(val[1]))
            radius = int(val[2])
            self.circles.append((val, center, radius))
            # print 'Found circle at %s with size %s' % (str(center), str(radius))
            
            # cv.Circle(self.output, center, radius, cv.RGB(255, 0, 0), 2, cv.CV_AA, 0)
        
        # if self.display_type == 'original':
        #     return self.image
        # 
        # if display_type == 'gray':
        #     return self.gray
        # 
        # if display_type == 'edges':
        #     return self.edges
        # 
        # if display_type == 'output':
        #     return self.output
        # 
        # return self.output
    
if __name__ == '__main__':
    
    pygame.init()

    screen = pygame.display.set_mode([640, 480])
    pygame.display.set_caption('OpenCV Circle Detection')
    
    font = pygame.font.Font(None, 24)
    
    monitor = Monitor()
    
    display_type = 'original'
    
    draw_circles = False
    
    clock = pygame.time.Clock()
    finished = False
    
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    display_type = 'gray'
                if event.key == pygame.K_o:
                    display_type = 'original'
                if event.key == pygame.K_e:
                    display_type = 'edges'
                if event.key == pygame.K_SPACE:
                    display_type = 'output'
                if event.key == pygame.K_c:
                    draw_circles = not draw_circles
                print display_type
                    
        screen.fill((0, 0, 0))

        monitor.capture()
        
        for circle in monitor.circles:
            print 'Found circle at %s with size %s' % (str(circle[1]), str(circle[2]))
        
        pygame_surface = monitor.get_image(display_type)
        
        screen.blit(pygame_surface, (0, 0))

        if draw_circles:
            for circle in monitor.circles:
                pygame.draw.circle(screen, (255, 0, 0), (circle[1][0], circle[1][1]), circle[2], 3)

        display_text = font.render(display_type, 1, (0, 0, 0))
        screen.blit(display_text, (10, 10))

        display_text = font.render(display_type, 1, (255, 255, 255))
        screen.blit(display_text, (11, 11))

        #  Render fps
        fps = str(clock.get_fps())
        fps_text = font.render(fps, 1, (0, 0, 0)) # Black
        screen.blit(fps_text, (10, 30))

        fps_text = font.render(fps, 1, (255, 255, 255)) # White
        screen.blit(fps_text, (11, 31))

        clock.tick(30)
        pygame.display.flip()
