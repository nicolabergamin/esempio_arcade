import arcade
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Square vs Triangles"

class Bullet:
    """Classe che rappresenta un proiettile sparato dai nemici"""
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        
        # Calcola la direzione verso il giocatore
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalizza il vettore e imposta la velocità
        self.speed = 300
        if distance > 0:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed
        else:
            self.vx = 0
            self.vy = 0
        
        self.radius = 5
        
    def update(self, delta_time):
        """Aggiorna la posizione del proiettile"""
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        
    def is_off_screen(self):
        """Controlla se il proiettile è uscito dallo schermo"""
        return (self.x < -50 or self.x > SCREEN_WIDTH + 50 or
                self.y < -50 or self.y > SCREEN_HEIGHT + 50)
                
    def collides_with_player(self, player_x, player_y, player_size):
        """Controlla la collisione con il giocatore"""
        half_size = player_size / 2
        return (player_x - half_size < self.x < player_x + half_size and
                player_y - half_size < self.y < player_y + half_size)

class Enemy:
    """Classe che rappresenta un nemico (triangolo rosso)"""
    def __init__(self):
        # Spawna su un bordo casuale dello schermo con un margine
        margin = 50
        edge = random.randint(0, 3)
        if edge == 0:  # alto
            self.x = random.randint(margin, SCREEN_WIDTH - margin)
            self.y = SCREEN_HEIGHT - margin
        elif edge == 1:  # destra
            self.x = SCREEN_WIDTH - margin
            self.y = random.randint(margin, SCREEN_HEIGHT - margin)
        elif edge == 2:  # basso
            self.x = random.randint(margin, SCREEN_WIDTH - margin)
            self.y = margin
        else:  # sinistra
            self.x = margin
            self.y = random.randint(margin, SCREEN_HEIGHT - margin)
            
        self.size = 30
        self.time_since_shot = 0
        
    def update(self, delta_time, shooting_speed):
        """Aggiorna il timer di sparo del nemico"""
        self.time_since_shot += delta_time
        return self.time_since_shot >= shooting_speed
        
    def reset_shot_timer(self):
        """Resetta il timer dopo aver sparato"""
        self.time_since_shot = 0

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        
        # Giocatore (quadrato blu)
        self.square_size = 50
        self.square_x = SCREEN_WIDTH / 2
        self.square_y = SCREEN_HEIGHT / 2
        self.speed = 200
        self.velocity_x = 0
        self.velocity_y = 0
        self.health = 3
        self.alive = True
        
        # Input tracking per controlli più fluidi
        self.keys_pressed = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        
        # Liste per nemici e proiettili
        self.enemies = []
        self.bullets = []
        
        # Timer per lo spawn dei nemici
        self.time_since_spawn = 0
        self.spawn_rate = 5.0  # Un nemico ogni 5 secondi
        self.shooting_speed = 3.0  # Nemici sparano ogni 3 secondi
        
    def on_draw(self):
        """Disegna tutti gli elementi del gioco"""
        self.clear()
        
        # Disegna il giocatore (quadrato blu)
        arcade.draw_lrbt_rectangle_filled(
            self.square_x - self.square_size / 2,
            self.square_x + self.square_size / 2,
            self.square_y - self.square_size / 2,
            self.square_y + self.square_size / 2,
            arcade.color.BLUE
        )
        
        # TODO 1: Cambia il colore del quadrato in base alla vita
        # Suggerimento: Crea una funzione get_player_color() che restituisce:
        # - BLUE se health == 3
        # - GREEN se health == 2
        # - YELLOW se health == 1
        # - BLACK se non è vivo
        # Poi usa questo colore invece di arcade.color.BLUE
        
        # Disegna i nemici (triangoli rossi)
        for enemy in self.enemies:
            arcade.draw_triangle_filled(
                enemy.x, enemy.y + enemy.size / 2,
                enemy.x - enemy.size / 2, enemy.y - enemy.size / 2,
                enemy.x + enemy.size / 2, enemy.y - enemy.size / 2,
                arcade.color.RED
            )
            
        # Disegna i proiettili come cerchi
        for bullet in self.bullets:
            arcade.draw_circle_filled(bullet.x, bullet.y, bullet.radius, arcade.color.DARK_RED)
        
        # Interfaccia utente
        arcade.draw_text(f"Vita: {self.health}", 10, SCREEN_HEIGHT - 30, 
                        arcade.color.BLACK, 20)
        arcade.draw_text(f"Nemici: {len(self.enemies)}", 10, SCREEN_HEIGHT - 60, 
                        arcade.color.BLACK, 20)
        
        # TODO 2: Mostra "GAME OVER" quando il giocatore muore
        # Suggerimento: Controlla se il giocatore è vivo, poi usa arcade.draw_text
        # per mostrare "GAME OVER" al centro dello schermo in rosso e grassetto
    
    def update_velocity(self):
        """Aggiorna la velocità in base ai tasti premuti"""
        self.velocity_x = 0
        self.velocity_y = 0
        
        if self.keys_pressed['up']:
            self.velocity_y = self.speed
        if self.keys_pressed['down']:
            self.velocity_y = -self.speed
        if self.keys_pressed['left']:
            self.velocity_x = -self.speed
        if self.keys_pressed['right']:
            self.velocity_x = self.speed
    
    def on_update(self, delta_time):
        """Aggiorna la logica del gioco ogni frame"""
        # TODO 3: Blocca il gioco quando il giocatore muore
        # Suggerimento: All'inizio di questa funzione, controlla se il giocatore è vivo
        # Se è False, usa 'return' per uscire subito e non aggiornare nulla
        
        # Aggiorna la posizione del giocatore
        self.square_x += self.velocity_x * delta_time
        self.square_y += self.velocity_y * delta_time
        
        # Mantieni il giocatore dentro lo schermo
        half_size = self.square_size / 2
        self.square_x = max(half_size, min(SCREEN_WIDTH - half_size, self.square_x))
        self.square_y = max(half_size, min(SCREEN_HEIGHT - half_size, self.square_y))
        
        # Spawn dei nemici
        self.time_since_spawn += delta_time
        if self.time_since_spawn >= self.spawn_rate:
            self.enemies.append(Enemy())
            self.time_since_spawn = 0

        # TODO 4: Lo chiamavano flash
        # Nelle righe qui sopra vediamo come fare in modo che "accada qualcosa ogni tot tempo"
        # Aggiungi una variabile "speed_increase_rate", impostala a 2 secondi. 
        # Ogni due secondi, aumenta la variabile "speed" del 10%

            
        # Aggiorna i nemici e gestisci gli spari
        for enemy in self.enemies:
            if enemy.update(delta_time, self.shooting_speed):
                # Il nemico spara verso il giocatore
                bullet = Bullet(enemy.x, enemy.y, self.square_x, self.square_y)
                self.bullets.append(bullet)
                enemy.reset_shot_timer()
                
        # Aggiorna i proiettili
        for bullet in self.bullets[:]:
            bullet.update(delta_time)
            
            # Controlla collisione con il giocatore
            if bullet.collides_with_player(self.square_x, self.square_y, self.square_size):
                self.health -= 1
                self.bullets.remove(bullet)
                if self.health <= 0:
                    self.alive = False
                    self.velocity_x = 0
                    self.velocity_y = 0
            # Rimuovi i proiettili fuori schermo
            elif bullet.is_off_screen():
                self.bullets.remove(bullet)

        
        
            
    # TODO 0: sembra che i controlli siano un po'... Strani. Riesci a sistemarli? 
    # Consiglio: Se fai partire il programma noterai che in realtà il movimento verso l'alto e verso il basso funziona
    # Bisogna sistemare solo il movimento a sinistra e destra
    def on_key_press(self, key, modifiers):
        """Gestisce la pressione dei tasti"""
        if key in [arcade.key.UP, arcade.key.W]:
            self.keys_pressed['up'] = True
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.keys_pressed['down'] = True
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.keys_pressed['righttttttttttt'] = True
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.keys_pressed['left'] = False
        
        self.update_velocity()
            
    def on_key_release(self, key, modifiers):
        """Gestisce il rilascio dei tasti"""
        if key in [arcade.key.UP, arcade.key.W]:
            self.keys_pressed['up'] = False
        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.keys_pressed['down'] = False
        elif key in [arcade.key.LEFT, arcade.key.A]:
            self.keys_pressed['right'] = False
        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.keys_pressed['left'] = True
        
        self.update_velocity()

def main():
    """Funzione principale che avvia il gioco"""
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()