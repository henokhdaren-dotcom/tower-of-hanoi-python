
import pygame
import sys

pygame.init()

# Konfigurasi game
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi - Game Development")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 36, bold=True)

# Warna
BACKGROUND = (245, 247, 250)
DARK = (35, 43, 60)
WHITE = (255, 255, 255)
GRAY = (160, 170, 185)
GREEN = (35, 170, 115)
RED = (220, 75, 75)
BLUE = (70, 130, 220)
YELLOW = (255, 195, 70)

# Posisi tiang
ROD_X = [180, 450, 720]
BASE_Y = 455
ROD_TOP = 160

# Tiga cakram: angka terbesar = cakram terbesar
TOTAL_DISKS = 3
DISK_COLORS = [
    (75, 145, 235),
    (55, 190, 150),
    (245, 165, 65),
    (215, 90, 115),
    (150, 105, 220),
]

def reset_game():
    global towers, moves, selected_rod, won, message

    towers = [
        list(range(TOTAL_DISKS, 0, -1)),
        [],
        []
    ]

    moves = 0
    selected_rod = None
    won = False
    message = "Pilih tiang asal, lalu pilih tiang tujuan."

reset_game()


def draw_text(text, font, color, x, y, center=True):
    image = font.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(image, rect)


def draw_button(rect, text):
    pygame.draw.rect(screen, BLUE, rect, border_radius=10)
    draw_text(text, SMALL_FONT, WHITE, rect.centerx, rect.centery)


def draw_game():
    screen.fill(BACKGROUND)

    draw_text("TOWER OF HANOI", BIG_FONT, DARK, WIDTH // 2, 45)
    draw_text(
        f"Jumlah Langkah: {moves}",
        FONT, DARK, WIDTH // 2, 95
    )

    # Gambar alas
    pygame.draw.rect(
        screen, (185, 193, 205),
        (55, BASE_Y, 790, 18),
        border_radius=5
    )

    # Gambar tiang
    for i, x in enumerate(ROD_X):
        pygame.draw.rect(
            screen, GRAY,
            (x - 7, ROD_TOP, 14, BASE_Y - ROD_TOP),
            border_radius=7
        )

        # Sorot tiang yang dipilih
        if selected_rod == i:
            pygame.draw.circle(
                screen, GREEN, (x, ROD_TOP - 18), 13
            )

        draw_text(
            ["A", "B", "C"][i],
            BIG_FONT, DARK, x, BASE_Y + 45
        )

        # Gambar cakram dari bawah ke atas
        for j, disk in enumerate(towers[i]):
            disk_width = 65 + disk * 35
            disk_height = 24

            x_pos = x - disk_width // 2
            y_pos = BASE_Y - (j + 1) * disk_height

            # Cakram terpilih diangkat sedikit
            if selected_rod == i and j == len(towers[i]) - 1:
                y_pos -= 15

            color = DISK_COLORS[(disk - 1) % len(DISK_COLORS)]

            rect = pygame.Rect(
                x_pos, y_pos, disk_width, disk_height - 3
            )

            pygame.draw.rect(
                screen, color, rect, border_radius=8
            )
            pygame.draw.rect(
                screen, WHITE, rect, width=2, border_radius=8
            )

    # Petunjuk
    draw_text(
        message, SMALL_FONT, DARK, WIDTH // 2, 535
    )

    draw_button(
        pygame.Rect(740, 20, 125, 38), "Reset Game"
    )

    if won:
        pygame.draw.rect(
            screen, WHITE,
            (190, 205, 520, 115),
            border_radius=18
        )
        pygame.draw.rect(
            screen, GREEN,
            (190, 205, 520, 115),
            width=3, border_radius=18
        )

        draw_text(
            "SELAMAT, KAMU MENANG!",
            BIG_FONT, GREEN, WIDTH // 2, 240
        )
        draw_text(
            f"Total langkah: {moves}",
            FONT, DARK, WIDTH // 2, 282
        )

    pygame.display.flip()


def get_clicked_rod(mouse_x):
    """Menentukan tiang berdasarkan posisi klik mouse."""
    for i, x in enumerate(ROD_X):
        if abs(mouse_x - x) < 100:
            return i
    return None


def move_disk(source, destination):
    global moves, message, won, selected_rod

    # Tidak bisa memindahkan ke tiang yang sama
    if source == destination:
        message = "Pilih tiang tujuan yang berbeda."
        return

    # Tiang asal harus memiliki cakram
    if not towers[source]:
        message = "Tiang asal masih kosong!"
        return

    disk = towers[source][-1]

    # Cek aturan ukuran cakram
    if towers[destination]:
        top_disk = towers[destination][-1]

        if disk > top_disk:
            message = "Gagal! Cakram besar tidak boleh di atas cakram kecil."
            return

    towers[source].pop()
    towers[destination].append(disk)

    moves += 1
    selected_rod = None
    message = "Bagus! Lanjutkan sampai semua cakram di tiang C."

    # Kondisi kemenangan
    if len(towers[2]) == TOTAL_DISKS:
        won = True
        message = "Permainan selesai!"


# Game loop utama
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos

                # Tombol reset
                reset_rect = pygame.Rect(740, 20, 125, 38)

                if reset_rect.collidepoint(mx, my):
                    reset_game()
                    continue

                if won:
                    continue

                # Klik tiang
                if ROD_TOP - 30 <= my <= BASE_Y + 15:
                    rod = get_clicked_rod(mx)

                    if rod is not None:
                        if selected_rod is None:
                            if towers[rod]:
                                selected_rod = rod
                                message = (
                                    "Sekarang pilih tiang tujuan."
                                )
                            else:
                                message = "Tiang tersebut kosong!"
                        else:
                            move_disk(selected_rod, rod)

    draw_game()
    clock.tick(60)

pygame.quit()
sys.exit()