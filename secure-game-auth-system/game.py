import pygame
import sys
from auth import login_user, register_user

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Secure Game System")

# Fonts and colors
FONT = pygame.font.Font(None, 32)
TITLE_FONT = pygame.font.Font(None, 48)
BG_COLOR = (20, 25, 40)
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
RED = (200, 50, 50)
GREEN = (50, 200, 100)
ACTIVE_COLOR = (255, 255, 0)  # yellow highlight for active box


# InputBox class for text input
class InputBox:
    def __init__(self, x, y, w, h, password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.password = password

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self):
        # Draw rectangle: yellow if active, white if inactive
        color = ACTIVE_COLOR if self.active else WHITE
        pygame.draw.rect(SCREEN, color, self.rect, 2)

        # Display text (mask password if needed)
        display_text = "*" * len(self.text) if self.password else self.text
        txt_surface = FONT.render(display_text, True, WHITE)
        SCREEN.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))


# Button class
class Button:
    def __init__(self, text, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE, self.rect)
        txt_surface = FONT.render(self.text, True, WHITE)
        SCREEN.blit(txt_surface, (self.rect.x + 20, self.rect.y + 10))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# Game screen after successful login
def start_game(username):
    while True:
        SCREEN.fill(BG_COLOR)
        welcome_text = TITLE_FONT.render(f"Welcome, {username}", True, GREEN)
        SCREEN.blit(welcome_text, (150, 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


# Main UI function
def start_ui():
    clock = pygame.time.Clock()

    # Input boxes
    username_box = InputBox(250, 120, 200, 40)
    password_box = InputBox(250, 180, 200, 40, password=True)

    # Buttons
    login_button = Button("Login", 170, 250, 100, 40)
    register_button = Button("Register", 330, 250, 100, 40)

    message = ""
    message_color = RED

    while True:
        SCREEN.fill(BG_COLOR)

        # Title
        title = TITLE_FONT.render("Secure Game Login", True, WHITE)
        SCREEN.blit(title, (150, 40))

        # Labels to the left of input boxes
        username_label = FONT.render("Username:", True, WHITE)
        password_label = FONT.render("Password:", True, WHITE)

        SCREEN.blit(username_label, (username_box.rect.x - 120, username_box.rect.y + 5))
        SCREEN.blit(password_label, (password_box.rect.x - 120, password_box.rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle input
            username_box.handle_event(event)
            password_box.handle_event(event)

            # Buttons
            if login_button.clicked(event):
                if login_user(username_box.text, password_box.text):
                    start_game(username_box.text)
                else:
                    message = "Login failed or account locked"
                    message_color = RED

            if register_button.clicked(event):
                register_user(username_box.text, password_box.text)
                message = "User registered"
                message_color = GREEN

        # Draw UI elements
        username_box.draw()
        password_box.draw()
        login_button.draw()
        register_button.draw()

        # Message
        msg_surface = FONT.render(message, True, message_color)
        SCREEN.blit(msg_surface, (200, 310))

        pygame.display.flip()
        clock.tick(60)
