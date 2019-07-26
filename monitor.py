from flask import Flask, request
import pygame
import cfg
app = Flask(__name__)

pygame.mixer.init()
beep_sound = pygame.mixer.Sound(config.effects_path / 'beep.wav')
beep = lambda: beep_sound.play() if not cfg.mute else None

@app.route('/monitor/', methods=['post'])
def monitor():
    data = request.get_json()
    print(data['created_at'], data['raw_command'])
    beep()
    return 'ok'