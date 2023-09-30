import pygame
from pygame.locals import *
import time 
import random

size = 40
Background_color = (110,110,5)

class apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("/Users/amitanand/Desktop/ML Codebasics/PyGame_Project/Resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size*3
        self.y = size*3
    
    def move(self):
        self.x =random.randint(1,31)*size
        self.y =random.randint(1,17)*size

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("/Users/amitanand/Desktop/ML Codebasics/PyGame_Project/Resources/block.jpg").convert() ##loading the Block image
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'left':
            self.x[0] -= size

        self.draw()


class Game:
    def __init__(self):
        pygame.init() #this .init() is used to initialize the whole module
        pygame.display.set_caption("Snake and Apple Game")
        pygame.mixer.init()

        self.play_background_music()
        self.surface = pygame.display.set_mode((1280,720)) #screen window size
        self.surface.fill((255,255,255)) #color code can be take from RGB color picker from Google
        self.snake = Snake(self.surface, 1)  #intial length of snake is 1 
        self.snake.draw()
        self.apple = apple(self.surface)
        self.apple.draw()
        self.high_score = 0  # Initialize high score to 0
        self.difficulty_level = 1  # Initialize difficulty level to 1

    def display_Score(self):
        font  = pygame.font.SysFont('arial', 30)
        score  = font.render(f"score: {self.snake.length}", True, (255, 255, 255))
        high_score = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        self.surface.blit(score,(800,10))
        self.surface.blit(high_score, (800, 50))

    def is_collision(self, x1, y1, x2,y2 ):
        if x1 >=x2 and x1<=x2+ size :
            if y1>=y2 and y1 < y2 + size:
                return True
        return False
    
    def play_background_music(self):
        pygame.mixer.music.load("/Users/amitanand/Desktop/ML Codebasics/PyGame_Project/Resources/Background_music.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("/Users/amitanand/Desktop/ML Codebasics/PyGame_Project/Resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play_sound(self, sound):
        sound  = pygame.mixer.Sound(f"/Users/amitanand/Desktop/ML Codebasics/PyGame_Project/Resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_Score()
        pygame.display.flip()

        # Snake colliding with Apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("Snake")
            self.snake.increase_length()
            self.apple.move()
            if self.snake.length > self.high_score:
                self.high_score = self.snake.length  # Update the high score if necessary

        # Snake colliding with Itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Collison Occured"
            
        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1280 and 0 <= self.snake.y[0] <= 720):
            self.play_sound('crash')
            raise "Hit the boundry error"
            
    def increase_difficulty(self):
        # Calculate the new sleep time based on the current difficulty level
        new_sleep_time = max(0.20 - (self.difficulty_level - 1) * 0.04, 0.04)
    
        # Adjust the game's sleep time
        time.sleep(new_sleep_time)


            

    def show_Game_over(self):
        self.render_background()
        font  = pygame.font.SysFont('arial', 30)
        line1  = font.render(f"Game is Over! Your Score is : {self.snake.length}", True, (255, 255, 255))

        # Display the high score above the player's score
        high_score = font.render(f"High Score: {self.high_score}", True, (255, 255, 255))

        self.surface.blit(line1, (350,300))
        self.surface.blit(high_score, (350, 350))  # Adjust the position as needed
        line2  = font.render(f"To Play again press Enter. To Exit press escape:",True,(255, 255, 255))
        self.surface.blit(line2, (350,400))
        pygame.display.flip()

        pygame.mixer.music.pause()
        
    def reset(self):
        self.snake = Snake(self.surface, 1)  #intial length of snake is 1 
        self.apple = apple(self.surface)

    def run(self):
        #Writing code for screen to stay until i press cross or escape
        running  = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key  == K_ESCAPE:
                        pygame.mixer.music.unpause()
                        running = False
                    
                
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()
             
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

                    # Check the current score and increase the difficulty every 5 scores
                    if self.snake.length % 5 == 0:
                        if self.snake.length / 5 > self.difficulty_level:
                            self.difficulty_level += 1
                            self.increase_difficulty()  # Implement this method to adjust game parameters

            except Exception as e:
                self.show_Game_over()
                pause = True
                self.reset()
            time.sleep(0.1)
    


if __name__ == "__main__":
    game = Game()
    game.run()

    
    