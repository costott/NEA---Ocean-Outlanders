import pygame

import settings
import tools

class HUD:
    """HUD on screen during run"""
    def __init__(self):
        self.screen = pygame.display.get_surface() # game screen for easy access

        self.crosshair = pygame.image.load("assets/crosshair.png").convert_alpha() # crosshair for mouse 
        self.crosshair = pygame.transform.rotozoom(self.crosshair, 0, settings.CROSSHAIR_SCALE) # scale to size
        self.crosshair_rect = self.crosshair.get_rect() # conatiner for crosshair for easy positionings

        self.info_font = pygame.font.Font(None, settings.HUD_INFO_FONT_SIZE)
    
    def draw(self) -> None:
        """draw the HUD"""
        # draw main hud elements  
        self.wave() 
        self.gold()

        self.enemy_health_bars()
        self.player_health_bar()

        # mouse invisible when it shouldn't be (happens when switching out of cannons state)
        if not pygame.mouse.get_visible() and settings.current_run.player_boat.state != "cannons":
            pygame.mouse.set_visible(True)

        if settings.current_run.player_boat.state == "steering":
            self.steering_hud()
        elif settings.current_run.player_boat.state == "sailing":
            self.sailing_hud()
        elif settings.current_run.player_boat.state == "cannons":
            self.cannons_hud()
    
    def steering_hud(self) -> None:
        """draws steering bar onto the screen"""
        # create main bar
        bar = pygame.Rect(0,0,settings.WIDTH*0.6,settings.HEIGHT*0.04)
        bar.center = (settings.WIDTH/2, settings.HEIGHT-3*bar.height)
        inner_bar = tools.scaled_rect(bar, 0.95, 0.7)

        # create square to represent current angle velocity
        current_square = pygame.Rect(0,bar.top,bar.height,bar.height)
        current_square.centerx = bar.centerx - (bar.width/2-current_square.width/2)*(
                                                            settings.current_run.player_boat.angle_velocity/
                                                            settings.BOAT_MAX_ANGLE_SPEED)
        inner_current_square = tools.scaled_rect(current_square, 0.7, 0.7)

        # create square in middle of bar
        middle_square = current_square.copy()
        middle_square.center = bar.center
        inner_middle_square = tools.scaled_rect(middle_square, 0.7, 0.7)
        
        # draw all elements
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, bar, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.BROWN, inner_bar, border_radius=settings.BAR_RADIUS)

        pygame.draw.rect(self.screen, settings.BROWN, middle_square, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.WHITE, inner_middle_square, border_radius=settings.BAR_RADIUS)
        
        pygame.draw.rect(self.screen, settings.DARK_BLUE, current_square, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, inner_current_square, border_radius=settings.BAR_RADIUS)

    def sailing_hud(self) -> None:
        """draws the sailing bar onto the screen"""
        # create main bar
        bar = pygame.Rect(0,0,settings.WIDTH*0.04,settings.HEIGHT*0.6)
        bar.center = (settings.WIDTH-bar.width, settings.HEIGHT/2)
        inner_bar = tools.scaled_rect(bar, 0.7, 0.95)

        # create square to represent current speed
        current_square = pygame.Rect(bar.left,0,bar.width,bar.width)
        current_square.centery = bar.bottom - current_square.width/2 - (bar.height-current_square.width)*(
            settings.current_run.player_boat.speed/settings.current_run.player_boat.max_speed)
        inner_current_square = tools.scaled_rect(current_square, 0.7, 0.7)

        # create sqaure at bottom of bar
        bottom_square = current_square.copy()
        bottom_square.bottom = bar.bottom
        inner_bottom_square = tools.scaled_rect(bottom_square, 0.7, 0.7)

        # draw all elements
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, bar, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.BROWN, inner_bar, border_radius=settings.BAR_RADIUS)

        pygame.draw.rect(self.screen, settings.BROWN, bottom_square, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.WHITE, inner_bottom_square, border_radius=settings.BAR_RADIUS)
        
        pygame.draw.rect(self.screen, settings.DARK_BLUE, current_square, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, inner_current_square, border_radius=settings.BAR_RADIUS)

    def cannons_hud(self) -> None:
        """draws the HUD elements for the cannon"""
        if pygame.mouse.get_visible():      # mouse is visible
            pygame.mouse.set_visible(False) # make mouse invisible as crosshair will replace it

        self.crosshair_rect.center = pygame.mouse.get_pos()   # position crosshair at mouse
        self.screen.blit(self.crosshair, self.crosshair_rect) # draw crosshair to screen
    
    def wave(self) -> None:
        """draw the wave information (time+wave) to the screen"""
        # get time into h:m:s
        time = int(settings.current_run.time)
        time_hours = time // 3600
        time_minutes = (time - time_hours*3600) // 60
        time_seconds = round(time - (time_hours*3600+time_minutes*60))
        time_string = f"{time_hours:2}:{time_minutes:2}:{time_seconds:2}".replace(" ", "0")

        # make text and get rects
        time_text = self.info_font.render(time_string, True, settings.WHITE)
        time_rect = time_text.get_rect()
        wave_text = self.info_font.render(f"wave {settings.current_run.enemy_spawner.current_wave}", 
                                          True, settings.WHITE)
        wave_rect = wave_text.get_rect()

        # make container
        conainter_width = time_rect.width + settings.HUD_PADDING*3 + wave_rect.width 
        container_height = max(time_rect.height, wave_rect.height) + settings.HUD_PADDING
        container = pygame.Rect(0,0,conainter_width,container_height)
        inner_container = tools.scaled_rect(container, 0.95, 0.7)

        # position text
        time_rect.midleft = inner_container.midleft
        wave_rect.midright = inner_container.midright

        # draw elements to screen
        pygame.draw.rect(self.screen, settings.BROWN, container, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, inner_container, border_radius=settings.BAR_RADIUS)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(wave_text, wave_rect)
    
    def gold(self) -> None:
        """draw the gold information to the screen"""
        # make text and get rects
        gold_text = self.info_font.render(f"gold: {settings.current_run.gold}", True, settings.WHITE)
        gold_rect = gold_text.get_rect()

        # make container
        container_width = gold_rect.width + settings.HUD_PADDING 
        container_height = gold_rect.height + settings.HUD_PADDING 
        container = pygame.Rect(0,0,container_width,container_height)
        container.topright = (settings.WIDTH,0)
        inner_container = tools.scaled_rect(container, 0.9, 0.7)

        # position text
        gold_rect.center = container.center

        # draw elemts to screen
        pygame.draw.rect(self.screen, settings.BROWN, container, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, inner_container, border_radius=settings.BAR_RADIUS)
        self.screen.blit(gold_text, gold_rect)

    def enemy_health_bars(self) -> None:
        """draws all enemy health bars to the screen"""
        for boat in settings.current_run.boat_sprites:
            if boat == settings.current_run.player_boat: continue # ignore player boat
            
            # main bar
            bar = pygame.Rect(0,0,settings.ENEMY_HEALTH_BAR_WIDTH,settings.ENEMY_HEATH_BAR_HEIGHT)
            bar.center = pygame.math.Vector2(boat.rect.midtop)+settings.current_run.camera.camera_move
            bar.centery -= settings.ENEMY_HEALTH_BAR_OFFSET
            inner_bar = tools.scaled_rect(bar, 0.95, 0.6)

            # health bar
            health_bar_width = bar.width * (boat.hp/boat.start_hp)
            health_bar = pygame.Rect(0,0,health_bar_width,bar.height)
            health_bar.midleft = bar.midleft
            inner_health_bar = tools.scaled_rect(health_bar, 0.95, 0.6)

            # draw bars
            pygame.draw.rect(self.screen, settings.BROWN, bar, border_radius=settings.BAR_RADIUS)
            pygame.draw.rect(self.screen, settings.LIGHT_BROWN, inner_bar, border_radius=settings.BAR_RADIUS)

            pygame.draw.rect(self.screen, settings.BROWN, health_bar, border_radius=settings.BAR_RADIUS)
            pygame.draw.rect(self.screen, settings.RED, inner_health_bar, border_radius=settings.BAR_RADIUS)
    
    def player_health_bar(self) -> None:
        """draws player health bar to screen"""
        # create main bar
        bar = pygame.Rect(0,0,settings.WIDTH*0.6,settings.HEIGHT*0.04)
        bar.center = (settings.WIDTH/2, settings.HEIGHT-bar.height)
        inner_bar = tools.scaled_rect(bar, 0.98, 0.7)

        # health bar
        health_bar_width = bar.width * (settings.current_run.player_boat.hp/settings.GAME.player_stats.hp)
        health_bar = pygame.Rect(0,0,health_bar_width,bar.height)
        health_bar.midleft = bar.midleft
        inner_health_bar = tools.scaled_rect(health_bar, 0.98, 0.7)

        # draw bars
        pygame.draw.rect(self.screen, settings.BROWN, bar, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BROWN, inner_bar, border_radius=settings.BAR_RADIUS)

        pygame.draw.rect(self.screen, settings.BROWN, health_bar, border_radius=settings.BAR_RADIUS)
        pygame.draw.rect(self.screen, settings.LIGHT_BLUE, inner_health_bar, border_radius=settings.BAR_RADIUS)