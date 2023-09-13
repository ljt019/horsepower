import pygame
from constants import MAX_HORSEPOWER, MIN_DELAY, MAX_DELAY, NUM_FRAMES

class Animation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        
        # Load font for horsepower value on screen
        self.font = pygame.font.SysFont(None, 36)  # Change 36 to desired font size or None to default
        
        # Load all horse frames into a list
        self.horse_frames = [pygame.image.load(f'../resources/frame_{i}.png') for i in range(1, NUM_FRAMES + 1)]
        self.current_frame = 0  # To keep track of the current frame
        
        self.background = pygame.image.load('../resources/background.png')
        self.background_pos = [0, 0]

        # Load sound
        self.sound = pygame.mixer.Sound('../resources/galloping.wav')
        self.sound.play(-1)  # Play the sound in an infinite loop
        self.sound.set_volume(0)  # Start with sound muted

        self.frame_update_counter = 0  # Counter to keep track of frame updates

    def run_animation(self, horsepower):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Adjust background scroll speed based on horsepower
        speed = horsepower * 5  # Adjust multiplier as needed for desired effect
        self.background_pos[0] -= speed

        if abs(self.background_pos[0]) > self.background.get_width():
            self.background_pos[0] += self.background.get_width()

        # Draw background twice for continuous scrolling effect
        self.screen.blit(self.background, tuple(self.background_pos))
        self.screen.blit(self.background, (self.background_pos[0] + self.background.get_width(), self.background_pos[1]))

        # Draw current horse frame in the center
        horse_x = (self.screen.get_width() - self.horse_frames[self.current_frame].get_width()) // 2
        horse_y = (self.screen.get_height() - self.horse_frames[self.current_frame].get_height()) // 2
        self.screen.blit(self.horse_frames[self.current_frame], (horse_x, horse_y))
        
        # Calculate frame update delay based on horsepower
        if horsepower > 0:
            frame_update_delay = MAX_DELAY - ((MAX_DELAY - MIN_DELAY) * (horsepower / MAX_HORSEPOWER))
            frame_update_delay = int(round(frame_update_delay))
        else:
            frame_update_delay = MAX_DELAY

        # Update counter and check if it's time to switch frame
        self.frame_update_counter += 1
        if self.frame_update_counter >= frame_update_delay:
            self.current_frame = (self.current_frame + 1) % len(self.horse_frames)
            self.frame_update_counter = 0  # Reset the counter
        
        # Render the horsepower text
        text = self.font.render(f"Horsepower: {horsepower:.2f}", True, (255, 255, 255))  # White color
        text_rect = text.get_rect(center=(self.screen.get_width() / 2, 30))  # Positioned at the center top
        self.screen.blit(text, text_rect)
        
        pygame.display.flip()

        # Adjust sound volume based on horsepower
        volume = max(0, min(1, horsepower / MAX_HORSEPOWER))
        self.sound.set_volume(volume)
