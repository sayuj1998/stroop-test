import pygame
import random
import time

class StroopTest:
    """Stroop Test game for SXU to measure reaction time and cognitive interference."""

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 50
    BUTTON_PADDING = 30
    KEY_REPEAT_DELAY = 200
    KEY_REPEAT_INTERVAL = 50

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    COLORS = [RED, GREEN, BLUE, YELLOW]
    COLOR_NAMES = ["RED", "GREEN", "BLUE", "YELLOW"]

    def __init__(self) -> None:
        """Initialize game settings, fonts, and variables."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Stroop Test")

        self.font = pygame.font.Font(None, 75)
        self.button_font = pygame.font.Font(None, 50)
        self.input_font = pygame.font.Font(None, 50)

        self.reaction_times = []
        self.incorrect_count = 0
        self.user_name = ""

    def display_text(self, text, color, x, y) -> None:
        """
        Display text centered on the screen.
        Args:
            text: Text to display.
            color: RGB color of the text.
            x: X-coordinate for centering.
            y: Y-coordinate for centering.
        """
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, color, x, y, width, height) -> None:
        """
        Draw a button with a label.
        Args:
            text: Button label.
            color: Button color.
            x: X-coordinate of the top-left corner.
            y: Y-coordinate of the top-left corner.
            width: Button width.
            height: Button height.
        """
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.button_font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def draw_buttons(self, buttons) -> None:
        """Draw a list of buttons based on their properties."""
        for button_x, button_y, button_width, button_height, color_name in buttons:
            color_index = self.COLOR_NAMES.index(color_name)
            self.draw_button(color_name, self.COLORS[color_index], button_x, button_y, button_width, button_height)

    def get_random_color_and_text(self) -> tuple:
        """Generate a random color and color name."""
        color = random.choice(self.COLORS)
        text = random.choice(self.COLOR_NAMES)
        return color, text

    def check_button_click(self, pos, buttons) -> tuple:
        """
        Check if a button was clicked.
        Args:
            pos: Mouse click position (x, y).
            buttons: List of button properties (x, y, name).
        """
        for button in buttons:
            x, y, width, height, color_name = button
            if x <= pos[0] <= x + width and y <= pos[1] <= y + height:
                return color_name
        return None

    def get_user_name(self) -> bool:
        """Prompt the user to enter their name."""
        self.screen.fill(self.BLACK)
        input_box = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2 - 25, 200, 50)
        go_button = pygame.Rect(self.SCREEN_WIDTH // 2 - 75, self.SCREEN_HEIGHT // 2 + 50, 150, 50)
        color = pygame.Color('white')
        active = False
        text = ''
        done = False
        pygame.key.set_repeat(self.KEY_REPEAT_DELAY, self.KEY_REPEAT_INTERVAL)

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    elif go_button.collidepoint(event.pos) and text:
                        self.user_name = text
                        done = True
                if event.type == pygame.KEYDOWN and active:
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
            self.display_text("Welcome to the Stroop Test", self.WHITE, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 180)
            self.display_text("Enter your name:", self.WHITE, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 100)
            self.draw_button("Go", self.GREEN, go_button.x, go_button.y, go_button.width, go_button.height)
            pygame.display.flip()

        return False

    def run_test(self, trials) -> bool:
        """
        Run the Stroop Test.

        Args:
            trials: Number of trials to run.
        """
        self.reaction_times = []
        self.incorrect_count = 0

        for _ in range(trials):
            self.screen.fill(self.BLACK)
            color, text = self.get_random_color_and_text()
            self.display_text(text, color, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2.2)

            # Calculate button positions
            buttons = []
            button_y = self.SCREEN_HEIGHT - self.BUTTON_HEIGHT - 20
            button_x_start = (self.SCREEN_WIDTH - (self.BUTTON_WIDTH * 4 + self.BUTTON_PADDING * 3)) // 2
            for i, color_name in enumerate(self.COLOR_NAMES):
                button_x = button_x_start + i * (self.BUTTON_WIDTH + self.BUTTON_PADDING)
                buttons.append((button_x, button_y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, color_name))

            self.draw_buttons(buttons)
            pygame.display.flip()
            start_time = time.time()

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

            end_time = time.time()
            reaction_time = end_time - start_time
            correct_color_name = self.COLOR_NAMES[self.COLORS.index(color)]

            self.screen.fill(self.BLACK)
            if user_input == correct_color_name:
                self.reaction_times.append(reaction_time)
                self.display_text(f"Correct!", self.GREEN, self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
            else:
                self.incorrect_count += 1
                self.display_text(f"Incorrect! The color was {correct_color_name}", self.RED,
                                  self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

            pygame.display.flip()
            pygame.time.wait(2000)

        return False

    def save_reaction_times(self, filename: str) -> None:
        """
        Save reaction times and incorrect answers to a file.
        Args:
            filename: Name of the file to save the results.
        """
        with open(filename, 'a') as file:
            if not self.reaction_times:
                file.write(f"Name: {self.user_name} | No correct answers recorded.\n")
                file.write(f"Name: {self.user_name} | Incorrect answers: {self.incorrect_count}\n\n")
                return

            for i, reaction_time in enumerate(self.reaction_times, 1):
                file.write(f"Name: {self.user_name} | Trial: {i} | Reaction time: {reaction_time:.6f} seconds\n")

            avg_reaction_time = sum(self.reaction_times) / len(self.reaction_times)
            file.write(f"Name: {self.user_name} | Average Reaction time: {avg_reaction_time:.6f} seconds\n")
            file.write(f"Name: {self.user_name} | Incorrect answers: {self.incorrect_count}\n\n")

if __name__ == "__main__":
    filename = 'reaction_times.txt'
    stroop_test = StroopTest()

    while True:
        if stroop_test.get_user_name():
            break
        if stroop_test.run_test(trials=4):
            break
        stroop_test.save_reaction_times(filename)

    pygame.quit()
    print(f"Reaction times saved to {filename}")