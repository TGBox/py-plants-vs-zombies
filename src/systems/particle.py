"""
Particle and visual effects system for hit effects, explosions, and floating text.
"""

import math
import random
import pygame


class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: tuple[int, int, int],
        radius: float,
        lifetime: float,
        gravity: float = 0.0,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.gravity = gravity

    def update(self, dt: float) -> bool:
        self.lifetime -= dt
        if self.lifetime <= 0:
            return False
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        return True

    def render(self, surface: pygame.Surface):
        progress = max(0.0, self.lifetime / self.max_lifetime)
        current_rad = max(1.0, self.radius * progress)
        alpha = int(255 * progress)
        # Draw particle circle
        p_surf = pygame.Surface((int(current_rad * 2 + 2), int(current_rad * 2 + 2)), pygame.SRCALPHA)
        color_with_alpha = (*self.color[:3], alpha)
        pygame.draw.circle(p_surf, color_with_alpha, (int(current_rad + 1), int(current_rad + 1)), int(current_rad))
        surface.blit(p_surf, (self.x - current_rad - 1, self.y - current_rad - 1))


class FloatingText:
    def __init__(self, text: str, x: float, y: float, color: tuple[int, int, int], font: pygame.font.Font, duration: float = 1.2):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        self.elapsed += dt
        self.y -= 25.0 * dt  # float upwards
        return self.elapsed < self.duration

    def render(self, surface: pygame.Surface):
        alpha_ratio = 1.0 - (self.elapsed / self.duration)
        alpha = int(255 * max(0.0, alpha_ratio))
        # Render text with shadow
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        shadow_surf = self.font.render(self.text, True, (20, 20, 20))
        shadow_surf.set_alpha(int(alpha * 0.7))
        surface.blit(shadow_surf, (self.x - text_surf.get_width() // 2 + 2, self.y + 2))
        surface.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y))


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []
        self.floating_texts: list[FloatingText] = []

    def spawn_splat(self, x: float, y: float, is_ice: bool = False):
        color = (130, 220, 255) if is_ice else (120, 220, 60)
        count = 10 if is_ice else 8
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(50, 160)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(
                Particle(
                    x=x,
                    y=y,
                    vx=vx,
                    vy=vy,
                    color=color,
                    radius=random.uniform(3, 6),
                    lifetime=random.uniform(0.2, 0.4),
                    gravity=150.0,
                )
            )

    def spawn_explosion(self, x: float, y: float):
        colors = [(255, 60, 20), (255, 180, 30), (255, 240, 100), (80, 80, 80)]
        for _ in range(40):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(80, 320)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            c = random.choice(colors)
            self.particles.append(
                Particle(
                    x=x,
                    y=y,
                    vx=vx,
                    vy=vy,
                    color=c,
                    radius=random.uniform(5, 12),
                    lifetime=random.uniform(0.4, 0.8),
                    gravity=180.0,
                )
            )

    def spawn_sun_sparkles(self, x: float, y: float):
        for _ in range(8):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(40, 110)
            self.particles.append(
                Particle(
                    x=x,
                    y=y,
                    vx=math.cos(angle) * speed,
                    vy=math.sin(angle) * speed,
                    color=(255, 235, 80),
                    radius=random.uniform(3, 5),
                    lifetime=random.uniform(0.3, 0.5),
                    gravity=50.0,
                )
            )

    def add_floating_text(self, text: str, x: float, y: float, color: tuple[int, int, int], font: pygame.font.Font):
        self.floating_texts.append(FloatingText(text, x, y, color, font))

    def update(self, dt: float):
        self.particles = [p for p in self.particles if p.update(dt)]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]

    def render(self, surface: pygame.Surface):
        for p in self.particles:
            p.render(surface)
        for ft in self.floating_texts:
            ft.render(surface)
