import pygame
import random
import time
import os


class StroopTest:
    def __init__(self, user_name):
        self.user_name = user_name
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

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
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Stroop Test")

        # Set up font
        self.font = pygame.font.Font(None, 74)
        self.button_font = pygame.font.Font(None, 50)

        # Initialize reaction times list
        self.reaction_times = []

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

    def run_test(self, trials=10):
        for _ in range(trials):
            self.screen.fill(self.BLACK)

            # Get random color and text
            color, text = self.get_random_color_and_text()

            # Display the text
            self.display_text(text, color, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3)

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
                        pygame.quit()
                        return
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
            self.display_text(f"Reaction Time: {reaction_time:.3f} seconds", self.WHITE, self.SCREEN_WIDTH // 2,
                              self.SCREEN_HEIGHT // 2)
            pygame.display.flip()

            # Wait for a while before showing the next color
            pygame.time.wait(2000)

    def get_reaction_times(self):
        return self.reaction_times

    def save_reaction_times(self, filename):
        with open(filename, 'a') as file:
            for i, reaction_time in enumerate(self.reaction_times, 1):
                file.write(f"Name: {self.user_name} | Trial: {i} | Reaction time: {reaction_time:.6f} seconds\n")

            # Calculate and save the average reaction time
            avg_reaction_time = sum(self.reaction_times) / len(self.reaction_times)
            file.write(f"Name: {self.user_name} | Trial: avg | Reaction time: {avg_reaction_time:.6f} seconds\n")
            file.write("\n")


if __name__ == "__main__":
    user_name = input("Enter your name: ")
    trials = 10  # Number of trials for the test
    filename = 'reaction_times.txt'  # Output file

    stroop_test = StroopTest(user_name)
    stroop_test.run_test(trials)
    stroop_test.save_reaction_times(filename)
    print(f"Reaction times saved to {filename}")