import sys
import pygame
from bullet import Bullet
from aliens import Alien
from time import sleep

# 响应按键和鼠标事件
def check_events(ai_settings,screen,ship,bullets):
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        check_keydown(event,ai_settings,screen,ship,bullets)
      elif event.type == pygame.KEYUP:
        check_keyup(event,ship)

# 键盘抬起
def check_keyup(event, ship):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  elif event.key == pygame.K_LEFT:
    ship.moving_left = False
# 键盘按下
def check_keydown(event,ai_settings,screen,ship,bullets):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  elif event.key == pygame.K_LEFT:
    ship.moving_left = True
  elif event.key == pygame.K_SPACE:
    fire(ai_settings,screen,ship,bullets)
  elif event.key == pygame.K_q:
    sys.exit()

def update_screen(ai_settings,screen,ship,aliens,bullets):
  screen.fill(ai_settings.bg_color)
  for bullet in bullets.sprites():
    bullet.draw()
  ship.blitme()
  aliens.draw(screen)
  pygame.display.flip()

# 更新子弹位置
def update_bullets(ai_settings,screen,ship,aliens,bullets):
  bullets.update()
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)
  check_collisons(ai_settings, screen, ship, aliens, bullets)

def check_collisons(ai_settings,screen,ship,aliens,bullets):
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
  if len(aliens) == 0:
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)

def fire(ai_settings,screen,ship,bullets):
  if len(bullets) < ai_settings.bullet_allowd:
    new_Bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_Bullet)

def create_fleet(ai_settings, screen,ship,aliens):
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  number_alien_x = get_number_aliens_x(ai_settings,alien_width)
  number_row = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
  for r in range(number_row):
    for i in range(number_alien_x):
      create_alien(ai_settings,screen,aliens,i,r)

# 计算每一行容纳的包子数
def get_number_aliens_x(ai_settings,alien_width):
  avaliable_space_x = ai_settings.screen_width - 2 * alien_width
  number_alien_x = int(avaliable_space_x / (2 * alien_width))
  return  number_alien_x

def get_number_rows(ai_settings,ship_height, alien_height):
  space_y = (ai_settings.screen_height - ship_height - 3*alien_height)
  return int(space_y/(2*alien_height))

# 创建一个包子
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
  alien = Alien(ai_settings,screen)
  alien_width = alien.rect.width
  alien.x = alien_width + alien_number*(2*alien_width)
  alien.rect.x = alien.x
  alien.rect.y = alien.rect.height + row_number*2*alien.rect.height
  aliens.add(alien)

def check_fleet_edges(ai_settings,aliens):
  for alien in aliens.sprites():
    if alien.check_edges():
      change_fleet_direction(ai_settings,aliens)
      break

def change_fleet_direction(ai_settings,aliens):
  for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed
  ai_settings.fleet_direction *= -1

# 更新包子位置
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
  check_fleet_edges(ai_settings,aliens)
  aliens.update()
  if pygame.sprite.spritecollideany(ship,aliens):
    ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
  check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
  if stats.ships_left > 0:
    stats.ships_left -= 1
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()
    sleep(0.5)
  else:
    stats.game_active = False

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
  screen_rect = screen.get_rect()
  for alien in aliens:
    if alien.rect.bottom >= screen_rect.bottom:
      ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
      break
