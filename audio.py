from os.path import join
from pyglet import media

laser = media.StaticSource(
    media.load(
        join(
            'sound_FX',
            'Digital_SFX_Set',
            'laser6.mp3'
        )
    )
)

powerup = media.StaticSource(
    media.load(
        join(
            'sound_FX',
            'Digital_SFX_Set',
            'powerUp6.mp3'
        )
    )
)

projectile_generate_one = media.StaticSource(
    media.load(
        join(
            'sound_FX',
            'Digital_SFX_Set',
            'phaseJump2.mp3'
        )
    )
)

sword_slice = media.StaticSource(
    media.load(
        join(
            'sound_FX',
            'freesound.org',
            'sword_slice.wav'
        )
    )
)

sword_sharpen = media.StaticSource(
    media.load(
        join(
            'sound_FX',
            'freesound.org',
            'sword_sharpen.wav'
        )
    )
)

explosion = media.StaticSource(
    media.load(
        join(
            'sound_FX',
            'freesound.org',
            'explosion.wav'
        )
    )
)