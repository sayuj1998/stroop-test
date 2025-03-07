import pygame
import random
import time
import os

class StroopTest:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 800

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        self.COLORS = [self.RED, self.GREEN, self.BLUE, self.YELLOW]
        self.COLOR_NAMES = ["RED", "GREEN", "BLUE", "YELLOW"]

        # Button dimensions
        self.BUTTON_WIDTH = 150
        self.BUTTON_HEIGHT = 50

        # Set up the display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Stroop Test")

        # Set up font
        self.font = pygame.font.Font(None, 75)
        self.button_font = pygame.font.Font(None, 50)
        self.input_font = pygame.font.Font(None, 50)

        # Initialize reaction times list
        self.reaction_times = []

        # Initialize user name
        self.user_name = ""

    def display_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, color, x, y, width, height):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.button_font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def get_random_color_and_text(self):
        color = random.choice(self.COLORS)
        text = random.choice(self.COLOR_NAMES)
        return color, text

    def check_button_click(self, pos, buttons):
        for button in buttons:
            x, y, width, height, color_name = button
            if x <= pos[0] <= x + width and y <= pos[1] <= y + height:
                return color_name
        return None

    def get_user_name(self):
        self.screen.fill(self.BLACK)
        input_box = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 - 25, 200, 50)
        go_button = pygame.Rect(self.SCREEN_WIDTH // 2 - 75, self.SCREEN_HEIGHT // 2 + 50, 150, 50)
        color_inactive = pygame.Color('white')
        color_active = pygame.Color('white')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    if go_button.collidepoint(event.pos) and text:
                        self.user_name = text
                        done = True
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN and text:
                            self.user_name = text
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill(self.BLACK)
            txt_surface = self.input_font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            self.display_text("Enter your name:", self.WHITE, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100)
            self.draw_button("Go", self.GREEN, go_button.x, go_button.y, go_button.width, go_button.height)
            pygame.display.flip()

        return False

    def run_test(self, trials=2):
        self.reaction_times = []  # Reset reaction times for each test

        for _ in range(trials):
            self.screen.fill(self.BLACK)

            # Get random color and text
            color, text = self.get_random_color_and_text()

            # Display the text
            self.display_text(text, color, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2.2)

            # Draw buttons
            buttons = []
            button_y = self.SCREEN_HEIGHT - self.BUTTON_HEIGHT - 20
            button_x_start = (self.SCREEN_WIDTH - (self.BUTTON_WIDTH * 4 + 30 * 3)) // 2
            for i, color_name in enumerate(self.COLOR_NAMES):
                button_x = button_x_start + i * (self.BUTTON_WIDTH + 30)
                self.draw_button(color_name, self.COLORS[i], button_x, button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
                buttons.append((button_x, button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, color_name))

            pygame.display.flip()

            # Record the start time
            start_time = time.time()

            # Wait for user input
            user_input = None
            while user_input is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        user_input = self.check_button_click(pos, buttons)
                        if user_input is None:
                            continue

            # Record the end time and calculate reaction time
            end_time = time.time()
            reaction_time = end_time - start_time
            self.reaction_times.append(reaction_time)

            # Display reaction time
            self.screen.fill(self.BLACK)
            self.display_text(f"Reaction Time: {reaction_time:.3f} seconds", self.WHITE, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
            pygame.display.flip()

            # Wait for a while before showing the next color
            pygame.time.wait(2000)

        return False

    def display_next_button(self):
        next_button = pygame.Rect(self.SCREEN_WIDTH // 2 - 75, self.SCREEN_HEIGHT - 100, 150, 50)
        self.draw_button("Next", self.GREEN, next_button.x, next_button.y, next_button.width, next_button.height)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if next_button.collidepoint(pos):
                        waiting = False

        return False

    def save_reaction_times(self, filename):
        with open(filename, 'a') as file:
            for i, reaction_time in enumerate(self.reaction_times, 1):
                file.write(f"Name: {self.user_name} | Trial: {i} | Reaction time: {reaction_time:.6f} seconds\n")

            # Calculate and save the average reaction time
            avg_reaction_time = sum(self.reaction_times) / len(self.reaction_times)
            file.write(f"Name: {self.user_name} | Average Reaction time: {avg_reaction_time:.6f} seconds\n")
            file.write("\n")

if __name__ == "__main__":
    filename = 'reaction_times.txt'  # Output file
    stroop_test = StroopTest()

    while True:
        if stroop_test.get_user_name():
            break
        if stroop_test.run_test(trials=2):  # Set to 2 trials for testing
            break
        stroop_test.save_reaction_times(filename)
        if stroop_test.display_next_button():
            break
    pygame.quit()
    print(f"Reaction times saved to {filename}")