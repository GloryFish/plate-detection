import sys
import cv
import pygame

class Monitor:
    
    
    def __init__(self):
        self.threshhold = 200
        self.save_images = False
        self.display_type = 'original'
        self.camera = cv.CaptureFromCAM(-1)
    
    def capture(self, filename = None):
        self.image = None
        
        if filename == None:
            # capture from open cv
            self.image = cv.QueryFrame(self.camera)
        else:
            self.image = cv.LoadImage(filename)
        
        self.output = cv.CloneImage(self.image)
        self.gray = cv.CreateImage(cv.GetSize(self.image), cv.IPL_DEPTH_8U, 1)
        self.edges = cv.CreateImage(cv.GetSize(self.image), cv.IPL_DEPTH_8U, 1)
    
        # Create a grayscale version
        cv.CvtColor(self.image, self.gray, cv.CV_BGR2GRAY)

    
        # Create an edge-detected version
        cv.Canny(self.gray, self.edges, self.threshhold, self.threshhold / 2, 3)

        hough_results = cv.CreateMat(640, 1, cv.CV_32FC3)
        
        cv.HoughCircles(self.gray, hough_results, cv.CV_HOUGH_GRADIENT, 2, self.gray.width / 18, self.threshhold, 300, 0, 0)

        for i in range(hough_results.rows):
            val = hough_results[i, 0]
            center = (int(val[0]), int(val[1]))
            radius = int(val[2])
            
            print 'Found circle at %s with size %s' % (str(center), str(radius))
            
            cv.Circle(self.output, center, radius, cv.RGB(255, 0, 0), 2, cv.CV_AA, 0)

        if self.save_images:
            cv.SaveImage('original.png', self.image)
            cv.SaveImage('gray.png', self.gray)
            cv.SaveImage('edges.png', self.edges)
            cv.SaveImage('output.png', self.output)
        
        if self.display_type == 'original':
            return self.image

        if display_type == 'gray':
            return self.gray

        if display_type == 'edges':
            return self.edges

        if display_type == 'output':
            return self.output
        
        return self.output
    
if __name__ == '__main__':
    
    pygame.init()

    screen = pygame.display.set_mode([640, 480])
    pygame.display.set_caption('OpenCV Circle Detection')
    
    font = pygame.font.Font(None, 24)
    
    
    monitor = Monitor()
    
    display_type = 'original'
    
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
                print display_type
                    
        screen.fill((0, 0, 0))

        # Convert OpenCv data to PyGame surface
        monitor.display_type = display_type
        image = monitor.capture()
        
        src_rgb = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
        if display_type == 'gray' or display_type == 'edges':
            cv.CvtColor(image, src_rgb, cv.CV_GRAY2RGB)
        else:        
            cv.CvtColor(image, src_rgb, cv.CV_BGR2RGB)

        pygame_surface = pygame.image.frombuffer(src_rgb.tostring(), cv.GetSize(src_rgb), "RGB")
        
        screen.blit(pygame_surface, (0, 0))

        display_text = font.render(display_type, 1, (0, 0, 0))
        screen.blit(display_text, (10, 10))

        display_text = font.render(display_type, 1, (255, 255, 255))
        screen.blit(display_text, (11, 11))

        #  Render fps
        fps = str(clock.get_fps())
        fps_text = font.render(fps, 1, (0, 0, 0))
        screen.blit(fps_text, (10, 30))

        fps_text = font.render(fps, 1, (255, 255, 255))
        screen.blit(fps_text, (11, 31))



        clock.tick(30)
        pygame.display.flip()
    
    
