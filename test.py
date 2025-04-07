import time
import pygame
import sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((240, 240))
pygame.display.set_caption("Timer & Stopwatch")
font = pygame.font.SysFont(None, 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Draw text
def draw_text(text, x, y):
    txt_surface = font.render(text, True, BLACK)
    screen.blit(txt_surface, (x, y))

# Button class
class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        draw_text(self.text, self.rect.x + 5, self.rect.y + 10)

    def is_pressed(self, pos):
        return self.rect.collidepoint(pos)

# Format time to HH:MM:SS
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Main app
def run_timer_app():
    mode = None
    running = False
    start_time = 0
    elapsed = 0
    timer_seconds = 0

    # Main buttons
    timer_btn = Button((20, 20, 90, 30), "Timer")
    sw_btn = Button((130, 20, 90, 30), "Stopwatch")
    start_btn = Button((20, 190, 60, 30), "Start")
    stop_btn = Button((90, 190, 60, 30), "Stop")
    reset_btn = Button((160, 190, 60, 30), "Reset")

    # Increment buttons (only for timer mode)
    inc_h1 = Button((20, 60, 50, 30), "+1h")
    inc_h5 = Button((20, 95, 50, 30), "+5h")
    inc_m1 = Button((80, 60, 50, 30), "+1m")
    inc_m5 = Button((80, 95, 50, 30), "+5m")
    inc_s1 = Button((140, 60, 50, 30), "+1s")
    inc_s5 = Button((140, 95, 50, 30), "+5s")

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if timer_btn.is_pressed(pos):
                    mode = "Timer"
                    elapsed = 0
                    timer_seconds = 0
                    running = False
                elif sw_btn.is_pressed(pos):
                    mode = "Stopwatch"
                    elapsed = 0
                    running = False
                elif start_btn.is_pressed(pos):
                    if not running:
                        start_time = time.time() - elapsed
                        running = True
                elif stop_btn.is_pressed(pos):
                    if running:
                        elapsed = time.time() - start_time
                        running = False
                elif reset_btn.is_pressed(pos):
                    running = False
                    elapsed = 0
                    if mode == "Timer":
                        timer_seconds = 0

                # Increment timer buttons
                if mode == "Timer" and not running:
                    if inc_h1.is_pressed(pos):
                        timer_seconds += 3600
                    elif inc_h5.is_pressed(pos):
                        timer_seconds += 5 * 3600
                    elif inc_m1.is_pressed(pos):
                        timer_seconds += 60
                    elif inc_m5.is_pressed(pos):
                        timer_seconds += 5 * 60
                    elif inc_s1.is_pressed(pos):
                        timer_seconds += 1
                    elif inc_s5.is_pressed(pos):
                        timer_seconds += 5

        # Update elapsed time
        if running:
            elapsed = time.time() - start_time

        # Display current mode and time
        if mode:
            draw_text(f"Mode: {mode}", 70, 135)
            current_time = timer_seconds - elapsed if mode == "Timer" else elapsed
            current_time = max(0, current_time)
            draw_text(format_time(current_time), 65, 160)

        # Draw common buttons
        timer_btn.draw()
        sw_btn.draw()
        start_btn.draw()
        stop_btn.draw()
        reset_btn.draw()

        # Draw timer increment buttons
        if mode == "Timer" and not running:
            inc_h1.draw()
            inc_h5.draw()
            inc_m1.draw()
            inc_m5.draw()
            inc_s1.draw()
            inc_s5.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(30)

if __name__ == '__main__':
    run_timer_app()
