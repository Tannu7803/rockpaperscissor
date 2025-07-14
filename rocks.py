import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Fonts and colors
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Utility text drawer
def draw_text(text, x, y):
    render = font.render(text, True, BLACK)
    screen.blit(render, (x, y))

# Game choices
choices = ["rock", "paper", "scissors"]

# Load images
rock_img = pygame.transform.scale(pygame.image.load("Rock.png"), (100, 100))
paper_img = pygame.transform.scale(pygame.image.load("paper.jpg"), (100, 100))
scissors_img = pygame.transform.scale(pygame.image.load("scissors.jpg"), (100, 100))
smile_img = pygame.transform.scale(pygame.image.load("smile.jpg"), (200, 200))
sad_img = pygame.transform.scale(pygame.image.load("sad.webp"), (200, 200))
background_img = pygame.transform.scale(pygame.image.load("bg.image.jpg"), (800, 600))
final_img = pygame.transform.scale(pygame.image.load("bgback.jpg"), (800, 600))
ins_img = pygame.transform.scale(pygame.image.load("bginst.jpg"), (800, 600))

# Load sounds
click_sound = pygame.mixer.Sound("click.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("loss.wav")

# Button class
class Button:
    def __init__(self, text, x, y, w=200, h=50):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(screen, (180, 180, 180), self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game logic
def get_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "You"
    else:
        return "Computer"

# Show instructions
def show_instructions():
    screen.blit(ins_img, (0, 0))
    lines = [
        "Instructions:",
        "1. First to win 3 rounds out of 5 wins the game.",
        "2. Click on Rock, Paper, or Scissors to make a move.",
        "3. If no choice is made in 3 seconds, computer auto-selects.",
        "4. After each round, scores are updated.",
        "5. Sound effects play on win/loss."
    ]

    for i, line in enumerate(lines):
        txt = small_font.render(line, True, BLACK)
        screen.blit(txt, (50, 80 + i * 40))
    pygame.display.update()
    time.sleep(5)

# ✅ Updated Final result screen (centered elements)
def show_final_screen(winner):
    screen.blit(final_img, (0, 0))

    if winner == "You":
        pygame.mixer.Sound.play(win_sound)
        img = smile_img
        msg = "🎉 You Win!"
    else:
        pygame.mixer.Sound.play(lose_sound)
        img = sad_img
        msg = "😢 You Lose!"

    # Centered text
    text_surface = font.render(msg, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 60))
    screen.blit(text_surface, text_rect)

    # Centered image
    img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(img, img_rect)

    # Restart Button (centered)
    again_btn = Button("Restart Game", WIDTH // 2 - 100, HEIGHT // 2 + 150)
    again_btn.draw()

    pygame.display.update()

    # Wait for button click or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if again_btn.is_clicked(pygame.mouse.get_pos()):
                    pygame.mixer.Sound.play(click_sound)
                    return  # restart game

# Start screen
def show_start_screen():
    start_btn = Button("Start Game", 250, 200)
    instr_btn = Button("Instructions", 250, 270)
    while True:
        screen.blit(background_img, (0, 0))
        start_btn.draw()
        instr_btn.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_btn.is_clicked(pos):
                    pygame.mixer.Sound.play(click_sound)
                    return "start"
                elif instr_btn.is_clicked(pos):
                    pygame.mixer.Sound.play(click_sound)
                    show_instructions()

# Main game
def main_game():
    player_score = 0
    comp_score = 0
    round_count = 0
    clock = pygame.time.Clock()

    while round_count < 5 and player_score < 3 and comp_score < 3:
        player_choice = None
        comp_choice = None
        selected = False
        timer_start = time.time()
        current_index = 0

        while not selected and (time.time() - timer_start) < 3:
            remaining_time = 3 - int(time.time() - timer_start)
            temp_choice = choices[current_index % 3]

            screen.fill(WHITE)
            draw_text("Choose Your Move:", 230, 20)
            draw_text(f"Time left: {remaining_time}", 290, 250)
            draw_text(f"Your Score: {player_score}", 100, 300)
            draw_text(f"Computer Score: {comp_score}", 400, 300)
            draw_text("Your Choice:", 110, 330)
            draw_text("Computer's Choice:", 390, 330)

            # Show player's options
            screen.blit(rock_img, (100, 100))
            screen.blit(paper_img, (300, 100))
            screen.blit(scissors_img, (500, 100))

            # Show cycling computer choice
            if temp_choice == "rock":
                screen.blit(rock_img, (400, 370))
            elif temp_choice == "paper":
                screen.blit(paper_img, (400, 370))
            elif temp_choice == "scissors":
                screen.blit(scissors_img, (400, 370))

            pygame.display.update()
            pygame.time.delay(200)
            current_index += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 100 < x < 200 and 100 < y < 200:
                        player_choice = "rock"
                        selected = True
                    elif 300 < x < 400 and 100 < y < 200:
                        player_choice = "paper"
                        selected = True
                    elif 500 < x < 600 and 100 < y < 200:
                        player_choice = "scissors"
                        selected = True

        if not selected:
            player_choice = random.choice(choices)

        comp_choice = random.choice(choices)
        winner = get_winner(player_choice, comp_choice)

        screen.fill(WHITE)
        draw_text(f"Your Score: {player_score}", 100, 300)
        draw_text(f"Computer Score: {comp_score}", 400, 300)
        draw_text("Your Choice:", 110, 330)
        draw_text("Computer's Choice:", 390, 330)

        if player_choice == "rock":
            screen.blit(rock_img, (100, 370))
        elif player_choice == "paper":
            screen.blit(paper_img, (100, 370))
        elif player_choice == "scissors":
            screen.blit(scissors_img, (100, 370))

        if comp_choice == "rock":
            screen.blit(rock_img, (400, 370))
        elif comp_choice == "paper":
            screen.blit(paper_img, (400, 370))
        elif comp_choice == "scissors":
            screen.blit(scissors_img, (400, 370))

        draw_text(f"Result: {winner}", 250, 470)
        pygame.display.update()
        time.sleep(1)

        if winner == "You":
            player_score += 1
            pygame.mixer.Sound.play(win_sound)
        elif winner == "Computer":
            comp_score += 1
            pygame.mixer.Sound.play(lose_sound)
        else:
            pygame.mixer.Sound.play(click_sound)

        round_count += 1

    final_winner = "You" if player_score > comp_score else "Computer"
    show_final_screen(final_winner)

# Run game loop
if __name__ == "__main__":
    while True:
        action = show_start_screen()
        if action == "start":
            main_game()
