import sys
import math
import random
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ─── Constants ───────────────────────────────────────────────────────────────
W, H = 1280, 720
FPS  = 60

FACTIONS = {
    "Solaris": {
        "color": QColor(255, 180, 0),
        "base_pos": (120, 500),
        "target": "Lunara",
        "missiles": ["Sunfire-I", "Sunfire-II", "Solar Nuke"],
        "flag_colors": [(255,200,0),(255,120,0)],
    },
    "Lunara": {
        "color": QColor(150, 200, 255),
        "base_pos": (1160, 500),
        "target": "Solaris",
        "missiles": ["Moonshot-I", "Moonshot-II", "Lunar Nuke"],
        "flag_colors": [(100,180,255),(50,100,200)],
    },
    "Terrax": {
        "color": QColor(80, 200, 80),
        "base_pos": (640, 580),
        "target": "Voidex",
        "missiles": ["Earthspike-I", "Earthspike-II", "Terra Nuke"],
        "flag_colors": [(60,180,60),(30,120,30)],
    },
    "Voidex": {
        "color": QColor(180, 80, 255),
        "base_pos": (640, 120),
        "target": "Terrax",
        "missiles": ["Voidbolt-I", "Voidbolt-II", "Void Nuke"],
        "flag_colors": [(160,60,240),(80,20,160)],
    },
}

MISSILE_STATS = {
    "Sunfire-I":    {"speed": 5,  "damage": 20, "radius": 30, "color": QColor(255,200,0),   "nuke": False},
    "Sunfire-II":   {"speed": 8,  "damage": 40, "radius": 50, "color": QColor(255,140,0),   "nuke": False},
    "Solar Nuke":   {"speed": 4,  "damage": 100,"radius": 120,"color": QColor(255,80,0),    "nuke": True},
    "Moonshot-I":   {"speed": 6,  "damage": 20, "radius": 30, "color": QColor(180,220,255), "nuke": False},
    "Moonshot-II":  {"speed": 9,  "damage": 40, "radius": 50, "color": QColor(100,160,255), "nuke": False},
    "Lunar Nuke":   {"speed": 4,  "damage": 100,"radius": 120,"color": QColor(50,100,255),  "nuke": True},
    "Earthspike-I": {"speed": 5,  "damage": 20, "radius": 30, "color": QColor(100,220,100), "nuke": False},
    "Earthspike-II":{"speed": 7,  "damage": 40, "radius": 50, "color": QColor(50,180,50),   "nuke": False},
    "Terra Nuke":   {"speed": 3,  "damage": 100,"radius": 120,"color": QColor(20,140,20),   "nuke": True},
    "Voidbolt-I":   {"speed": 7,  "damage": 20, "radius": 30, "color": QColor(200,100,255), "nuke": False},
    "Voidbolt-II":  {"speed": 10, "damage": 40, "radius": 50, "color": QColor(160,50,240),  "nuke": False},
    "Void Nuke":    {"speed": 5,  "damage": 100,"radius": 120,"color": QColor(100,0,200),   "nuke": True},
}

LANGS = {
    "EN": {
        "title": "COSMIC WARS",
        "select_faction": "Select Faction",
        "select_missile": "Select Missile",
        "fire": "FIRE!",
        "hp": "HP",
        "score": "Score",
        "wind": "Wind",
        "angle": "Angle",
        "power": "Power",
        "game_over": "GAME OVER",
        "victory": "VICTORY!",
        "restart": "Restart",
        "theme": "Theme",
        "language": "Language",
        "nuke_warning": "☢ NUCLEAR LAUNCH DETECTED ☢",
        "ammo": "Ammo",
    },
    "FA": {
        "title": "جنگ‌های کیهانی",
        "select_faction": "انتخاب فراکسیون",
        "select_missile": "انتخاب موشک",
        "fire": "شلیک!",
        "hp": "سلامت",
        "score": "امتیاز",
        "wind": "باد",
        "angle": "زاویه",
        "power": "قدرت",
        "game_over": "بازی تمام شد",
        "victory": "پیروزی!",
        "restart": "شروع مجدد",
        "theme": "تم",
        "language": "زبان",
        "nuke_warning": "☢ پرتاب هسته‌ای شناسایی شد ☢",
        "ammo": "مهمات",
    },
    "ZH": {
        "title": "宇宙战争",
        "select_faction": "选择阵营",
        "select_missile": "选择导弹",
        "fire": "发射！",
        "hp": "血量",
        "score": "分数",
        "wind": "风速",
        "angle": "角度",
        "power": "力量",
        "game_over": "游戏结束",
        "victory": "胜利！",
        "restart": "重新开始",
        "theme": "主题",
        "language": "语言",
        "nuke_warning": "☢ 检测到核弹发射 ☢",
        "ammo": "弹药",
    },
}

THEMES = {
    "dark": {
        "bg":       QColor(15, 15, 30),
        "panel":    QColor(25, 25, 50),
        "text":     QColor(220, 220, 255),
        "accent":   QColor(80, 120, 255),
        "btn":      QColor(40, 40, 80),
        "btn_text": QColor(200, 200, 255),
        "ground":   QColor(30, 60, 30),
        "sky_top":  QColor(5, 5, 20),
        "sky_bot":  QColor(20, 20, 60),
        "hp_good":  QColor(0, 220, 80),
        "hp_bad":   QColor(220, 50, 50),
    },
    "light": {
        "bg":       QColor(200, 220, 255),
        "panel":    QColor(230, 235, 255),
        "text":     QColor(20, 20, 60),
        "accent":   QColor(60, 100, 220),
        "btn":      QColor(180, 200, 240),
        "btn_text": QColor(20, 20, 80),
        "ground":   QColor(100, 180, 80),
        "sky_top":  QColor(135, 190, 255),
        "sky_bot":  QColor(200, 230, 255),
        "hp_good":  QColor(0, 180, 60),
        "hp_bad":   QColor(200, 40, 40),
    },
}

# ─── Particle ────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, nuke=False):
        self.x = x
        self.y = y
        angle = random.uniform(0, math.tau)
        spd   = random.uniform(2, 12) * (3 if nuke else 1)
        self.vx = math.cos(angle) * spd
        self.vy = math.sin(angle) * spd
        self.life = random.randint(30, 80) * (2 if nuke else 1)
        self.max_life = self.life
        r, g, b = color.red(), color.green(), color.blue()
        self.color = QColor(r, g, b)
        self.size  = random.uniform(3, 10) * (2 if nuke else 1)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.15
        self.life -= 1

    def draw(self, p: QPainter):
        alpha = int(255 * self.life / self.max_life)
        c = QColor(self.color)
        c.setAlpha(alpha)
        p.setBrush(QBrush(c))
        p.setPen(Qt.PenStyle.NoPen)
        s = self.size * self.life / self.max_life
        p.drawEllipse(QPointF(self.x, self.y), s, s)

# ─── Missile ─────────────────────────────────────────────────────────────────
class Missile:
    def __init__(self, x, y, angle_deg, power, stats, faction_color):
        self.x = float(x)
        self.y = float(y)
        rad    = math.radians(angle_deg)
        spd    = stats["speed"] * power / 50
        self.vx = math.cos(rad) * spd
        self.vy = -math.sin(rad) * spd
        self.stats  = stats
        self.color  = stats["color"]
        self.active = True
        self.trail  = []

    def update(self, wind):
        self.trail.append((self.x, self.y))
        if len(self.trail) > 25:
            self.trail.pop(0)
        self.vx += wind * 0.01
        self.vy += 0.12
        self.x  += self.vx
        self.y  += self.vy
        if self.y > H + 50 or self.x < -100 or self.x > W + 100:
            self.active = False

    def draw(self, p: QPainter):
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(180 * i / len(self.trail))
            c = QColor(self.color)
            c.setAlpha(alpha)
            p.setBrush(QBrush(c))
            p.setPen(Qt.PenStyle.NoPen)
            r = 3 * i / len(self.trail)
            p.drawEllipse(QPointF(tx, ty), r, r)
        p.setBrush(QBrush(self.color))
        p.setPen(QPen(Qt.GlobalColor.white, 1))
        p.drawEllipse(QPointF(self.x, self.y), 6, 6)
        if self.stats["nuke"]:
            c2 = QColor(255, 255, 100, 80)
            p.setBrush(QBrush(c2))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(self.x, self.y), 14, 14)

# ─── Base ─────────────────────────────────────────────────────────────────────
class Base:
    def __init__(self, name, data):
        self.name   = name
        self.x, self.y = data["base_pos"]
        self.color  = data["color"]
        self.hp     = 200
        self.max_hp = 200
        self.flag_colors = data["flag_colors"]
        self.ammo   = {m: 5 for m in data["missiles"]}
        self.ammo[data["missiles"][-1]] = 2  # nukes limited

    def draw(self, p: QPainter, theme):
        # Platform
        grad = QLinearGradient(self.x - 40, self.y - 10, self.x + 40, self.y + 20)
        grad.setColorAt(0, self.color.darker(150))
        grad.setColorAt(1, self.color)
        p.setBrush(QBrush(grad))
        p.setPen(QPen(self.color.lighter(150), 2))
        p.drawRoundedRect(self.x - 40, self.y - 10, 80, 30, 6, 6)

        # Tower
        p.setBrush(QBrush(self.color.darker(120)))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(self.x - 8, self.y - 50, 16, 40)

        # Flag
        flag_pts = [
            QPointF(self.x + 8, self.y - 50),
            QPointF(self.x + 35, self.y - 38),
            QPointF(self.x + 8, self.y - 26),
        ]
        p.setBrush(QBrush(QColor(*self.flag_colors[0])))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawPolygon(flag_pts)

        # Name
        p.setPen(QPen(theme["text"]))
        f = QFont("Arial", 9, QFont.Weight.Bold)
        p.setFont(f)
        p.drawText(self.x - 40, self.y + 30, 80, 20, Qt.AlignmentFlag.AlignCenter, self.name)

        # HP bar
        bar_w = 80
        hp_ratio = max(0, self.hp / self.max_hp)
        p.setBrush(QBrush(theme["hp_bad"]))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(self.x - 40, self.y + 50, bar_w, 8, 3, 3)
        p.setBrush(QBrush(theme["hp_good"]))
        p.drawRoundedRect(self.x - 40, self.y + 50, int(bar_w * hp_ratio), 8, 3, 3)

# ─── Game Canvas ─────────────────────────────────────────────────────────────
class GameCanvas(QWidget):
    score_changed   = pyqtSignal(int)
    game_over_signal= pyqtSignal(str)
    nuke_signal     = pyqtSignal()

    def __init__(self, theme_name="dark", lang="EN"):
        super().__init__()
        self.theme_name = theme_name
        self.lang       = lang
        self.setMinimumSize(600, 400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._init_game()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000 // FPS)

        self.setMouseTracking(True)
        self.aim_pos = QPointF(0, 0)

    def _init_game(self):
        self.bases     = {n: Base(n, d) for n, d in FACTIONS.items()}
        self.missiles  = []
        self.particles = []
        self.score     = 0
        self.wind      = random.uniform(-3, 3)
        self.wind_timer= 0
        self.player_faction  = "Solaris"
        self.selected_missile= FACTIONS["Solaris"]["missiles"][0]
        self.angle  = 45.0
        self.power  = 60.0
        self.game_over   = False
        self.winner      = ""
        self.nuke_flash  = 0
        self.stars       = [(random.randint(0, W), random.randint(0, H//2),
                             random.uniform(0.5, 2)) for _ in range(120)]
        self.clouds      = [(random.randint(0, W), random.randint(30, 180),
                             random.uniform(0.3, 1.0)) for _ in range(8)]
        self.ai_timer    = 0

    @property
    def T(self):
        return THEMES[self.theme_name]

    @property
    def L(self):
        return LANGS[self.lang]

    def set_theme(self, name):
        self.theme_name = name
        self.update()

    def set_lang(self, lang):
        self.lang = lang
        self.update()

    def set_faction(self, name):
        self.player_faction   = name
        self.selected_missile = FACTIONS[name]["missiles"][0]
        self.update()

    def set_missile(self, name):
        self.selected_missile = name
        self.update()

    def set_angle(self, v):
        self.angle = float(v)
        self.update()

    def set_power(self, v):
        self.power = float(v)
        self.update()

    def fire(self):
        if self.game_over:
            return
        base = self.bases[self.player_faction]
        ammo = base.ammo.get(self.selected_missile, 0)
        if ammo <= 0:
            return
        base.ammo[self.selected_missile] -= 1
        stats = MISSILE_STATS[self.selected_missile]
        # direction toward target
        target_name = FACTIONS[self.player_faction]["target"]
        tb = self.bases[target_name]
        dx = tb.x - base.x
        angle = self.angle if dx > 0 else 180 - self.angle
        m = Missile(base.x, base.y - 50, angle, self.power, stats, base.color)
        self.missiles.append(m)
        if stats["nuke"]:
            self.nuke_signal.emit()
            self.nuke_flash = 30

    def _ai_fire(self, faction_name):
        base = self.bases[faction_name]
        target_name = FACTIONS[faction_name]["target"]
        if target_name == self.player_faction:
            tb = self.bases[target_name]
            missiles = FACTIONS[faction_name]["missiles"]
            available = [m for m in missiles if base.ammo.get(m, 0) > 0]
            if not available:
                return
            chosen = random.choice(available)
            base.ammo[chosen] -= 1
            stats = MISSILE_STATS[chosen]
            dx = tb.x - base.x
            angle = random.uniform(35, 65)
            if dx < 0:
                angle = 180 - angle
            power = random.uniform(50, 90)
            m = Missile(base.x, base.y - 50, angle, power, stats, base.color)
            self.missiles.append(m)
            if stats["nuke"]:
                self.nuke_flash = 30

    def _tick(self):
        if self.game_over:
            return
        cw = self.width()
        ch = self.height()
        sx = cw / W
        sy = ch / H

        # Wind change
        self.wind_timer += 1
        if self.wind_timer > FPS * 8:
            self.wind_timer = 0
            self.wind = random.uniform(-4, 4)

        # AI
        self.ai_timer += 1
        if self.ai_timer > FPS * 3:
            self.ai_timer = 0
            for fn in FACTIONS:
                if fn != self.player_faction:
                    if random.random() < 0.6:
                        self._ai_fire(fn)

        # Update missiles
        for m in self.missiles:
            m.update(self.wind)
            if not m.active:
                continue
            # Check hits
            for bn, base in self.bases.items():
                bx = base.x * sx
                by = base.y * sy
                mx = m.x
                my = m.y
                dist = math.hypot(mx - bx, my - by)
                hit_r = m.stats["radius"] * min(sx, sy)
                if dist < hit_r + 30:
                    m.active = False
                    dmg = m.stats["damage"]
                    base.hp = max(0, base.hp - dmg)
                    # Explosion
                    for _ in range(60 if m.stats["nuke"] else 25):
                        self.particles.append(Particle(mx, my, m.color, m.stats["nuke"]))
                    if m.stats["nuke"]:
                        self.nuke_flash = 40
                    # Score
                    if bn != self.player_faction:
                        self.score += dmg
                        self.score_changed.emit(self.score)
                    break

        self.missiles = [m for m in self.missiles if m.active]

        # Update particles
        for pt in self.particles:
            pt.update()
        self.particles = [pt for pt in self.particles if pt.life > 0]

        if self.nuke_flash > 0:
            self.nuke_flash -= 1

        # Check game over
        player_base = self.bases[self.player_faction]
        if player_base.hp <= 0:
            self.game_over = True
            self.winner = "AI"
            self.game_over_signal.emit("lose")
        all_enemies_dead = all(
            self.bases[fn].hp <= 0
            for fn in FACTIONS if fn != self.player_faction
        )
        if all_enemies_dead:
            self.game_over = True
            self.winner = self.player_faction
            self.game_over_signal.emit("win")

        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cw, ch = self.width(), self.height()
        sx, sy = cw / W, ch / H

        # Sky gradient
        grad = QLinearGradient(0, 0, 0, ch * 0.7)
        grad.setColorAt(0, self.T["sky_top"])
        grad.setColorAt(1, self.T["sky_bot"])
        p.fillRect(0, 0, cw, ch, grad)

        # Stars (dark only)
        if self.theme_name == "dark":
            for sx2, sy2, sr in self.stars:
                c = QColor(255, 255, 255, int(180 * sr / 2))
                p.setBrush(QBrush(c))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(QPointF(sx2 * sx, sy2 * sy), sr * min(sx, sy), sr * min(sx, sy))

        # Clouds
        for cx2, cy2, cs in self.clouds:
            c = QColor(255, 255, 255, 60 if self.theme_name == "dark" else 180)
            p.setBrush(QBrush(c))
            p.setPen(Qt.PenStyle.NoPen)
            for dx2 in [-20, 0, 20]:
                p.drawEllipse(QPointF((cx2 + dx2) * sx, cy2 * sy),
                              30 * cs * sx, 18 * cs * sy)

        # Ground
        ground_y = ch * 0.78
        grad2 = QLinearGradient(0, ground_y, 0, ch)
        grad2.setColorAt(0, self.T["ground"])
        grad2.setColorAt(1, self.T["ground"].darker(150))
        p.fillRect(0, int(ground_y), cw, ch - int(ground_y), grad2)

        # Grid lines on ground
        p.setPen(QPen(QColor(255, 255, 255, 20), 1))
        for i in range(0, cw, 60):
            p.drawLine(i, int(ground_y), i, ch)

        # Nuke flash
        if self.nuke_flash > 0:
            alpha = int(180 * self.nuke_flash / 40)
            p.fillRect(0, 0, cw, ch, QColor(255, 255, 200, alpha))

        # Scale painter for game objects
        p.save()
        p.scale(sx, sy)

        # Bases
        for bn, base in self.bases.items():
            base.draw(p, self.T)

        # Aim line
        if not self.game_over:
            pb = self.bases[self.player_faction]
            p.setPen(QPen(QColor(255, 255, 100, 120), 1, Qt.PenStyle.DashLine))
            rad = math.radians(self.angle)
            dx2 = FACTIONS[self.player_faction]["target"]
            tb  = self.bases[dx2]
            direction = 1 if tb.x > pb.x else -1
            ex = pb.x + math.cos(rad) * direction * 200
            ey = (pb.y - 50) - math.sin(rad) * 200
            p.drawLine(QPointF(pb.x, pb.y - 50), QPointF(ex, ey))

        # Missiles
        for m in self.missiles:
            m.draw(p)

        # Particles
        for pt in self.particles:
            pt.draw(p)

        p.restore()

        # HUD
        self._draw_hud(p, cw, ch)

        # Game over overlay
        if self.game_over:
            self._draw_game_over(p, cw, ch)

        p.end()

    def _draw_hud(self, p, cw, ch):
        # Wind indicator
        wind_x = cw // 2
        wind_y = 30
        p.setPen(QPen(self.T["text"], 2))
        f = QFont("Arial", 10)
        p.setFont(f)
        p.drawText(wind_x - 60, wind_y - 15, 120, 20,
                   Qt.AlignmentFlag.AlignCenter,
                   f"{self.L['wind']}: {self.wind:+.1f}")
        # Arrow
        arrow_len = int(abs(self.wind) * 10)
        direction = 1 if self.wind > 0 else -1
        p.setPen(QPen(QColor(100, 200, 255), 3))
        p.drawLine(wind_x, wind_y + 5, wind_x + direction * arrow_len, wind_y + 5)
        # Arrowhead
        p.drawLine(wind_x + direction * arrow_len, wind_y + 5,
                   wind_x + direction * (arrow_len - 8), wind_y)
        p.drawLine(wind_x + direction * arrow_len, wind_y + 5,
                   wind_x + direction * (arrow_len - 8), wind_y + 10)

    def _draw_game_over(self, p, cw, ch):
        p.fillRect(0, 0, cw, ch, QColor(0, 0, 0, 160))
        f = QFont("Arial", 48, QFont.Weight.Bold)
        p.setFont(f)
        if self.winner == self.player_faction:
            p.setPen(QPen(QColor(100, 255, 100)))
            p.drawText(0, 0, cw, ch, Qt.AlignmentFlag.AlignCenter, self.L["victory"])
        else:
            p.setPen(QPen(QColor(255, 80, 80)))
            p.drawText(0, 0, cw, ch, Qt.AlignmentFlag.AlignCenter, self.L["game_over"])

    def restart(self):
        self._init_game()
        self.update()

    def mouseMoveEvent(self, e):
        self.aim_pos = e.position()

# ─── Control Panel ────────────────────────────────────────────────────────────
class ControlPanel(QWidget):
    def __init__(self, canvas: GameCanvas):
        super().__init__()
        self.canvas = canvas
        self.setMinimumWidth(260)
        self.setMaximumWidth(320)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        self.title_lbl = QLabel()
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont("Arial", 18, QFont.Weight.Bold)
        self.title_lbl.setFont(f)
        layout.addWidget(self.title_lbl)

        # Theme toggle
        self.theme_btn = QPushButton()
        self.theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_btn)

        # Language
        lang_row = QHBoxLayout()
        for lang in ["EN", "FA", "ZH"]:
            btn = QPushButton(lang)
            btn.clicked.connect(lambda _, l=lang: self._set_lang(l))
            lang_row.addWidget(btn)
        layout.addLayout(lang_row)

        layout.addWidget(self._sep())

        # Faction
        self.faction_lbl = QLabel()
        layout.addWidget(self.faction_lbl)
        self.faction_combo = QComboBox()
        for fn in FACTIONS:
            self.faction_combo.addItem(fn)
        self.faction_combo.currentTextChanged.connect(self._faction_changed)
        layout.addWidget(self.faction_combo)

        # Missile
        self.missile_lbl = QLabel()
        layout.addWidget(self.missile_lbl)
        self.missile_combo = QComboBox()
        layout.addWidget(self.missile_combo)
        self.missile_combo.currentTextChanged.connect(
            lambda t: self.canvas.set_missile(t) if t else None)

        # Ammo display
        self.ammo_lbl = QLabel()
        layout.addWidget(self.ammo_lbl)

        layout.addWidget(self._sep())

        # Angle
        self.angle_lbl = QLabel()
        layout.addWidget(self.angle_lbl)
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setRange(10, 80)
        self.angle_slider.setValue(45)
        self.angle_slider.valueChanged.connect(self._angle_changed