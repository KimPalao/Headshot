"use strict";

class Sprite {

}

(function (d) {

    class Sprite {
        // x: number;
        // y: number;
        // speed: number;
        // _scale: number;
        // image: HTMLImageElement;
        // context: CanvasRenderingContext2D;

        constructor(src, x, y, speed, scale, context) {
            this.image = new Image();
            this._scale = scale;
            this.image.onload = () => {
                console.log('onload', this.image.width, this.image.height, this);
                // this.image.width = this.image.width * this.scale;
                // this.image.height = this.image.height * this.scale;
                // this.image.width *= scale;
                // this.image.height *= scale;
            };
            this.image.src = src;
            this.x = x;
            this.y = y;
            this.speed = speed;
            this.context = context;
            this.fps = 60;
            this.last_draw = (new Date()).getTime();
        }

        draw() {
            this.context.drawImage(
                this.image,
                0,
                0,
                this.image.width,
                this.image.height,
                this.x,
                this.y,
                this.image.width * this.scale,
                this.image.height * this.scale
            )
        }

        move(x, y) {
            this.x = x;
            this.y = y;
        }

        get scale() {
            return this._scale
        }

        set scale(value) {
            this._scale = value;
            // this.image.scale = value;
        }


    }

    const canvas = d.querySelector('#canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const context = canvas.getContext('2d');

    // const big_planet = new Image();
    const background = new Image();
    background.src = 'images/space/parallax-space-background.png';
    // console.log(background.width);
    const big_planet = new Sprite(
        'images/space/parallax-space-big-planet.png',
        window.innerWidth / 2,
        window.innerHeight / 2,
        1 / 3,
        1,
        context
    );
    const far_planets = new Sprite(
        'images/space/parallax-space-far-planets.png',
        0,
        0,
        1 / 10,
        1,
        context
    );
    far_planets.image.onload += () => {
        far_planets.move(
            window.innerWidth - far_planets.image.width,
            window.innerHeight - far_planets.image.height,
        );
    };
    const ring_planet = new Sprite(
        'images/space/parallax-space-ring-planet.png',
        100,
        0,
        1 / 5,
        1,
        context
    );
    ring_planet.image.onload += () => {
        ring_planet.y = window.innerHeight - ring_planet.image.height;
    };

    const space_stars = new Sprite(
        'images/space/parallax-space-stars.png',
        0,
        0,
        1 / 8,
        1,
        context
    );

    const objects = [
        space_stars,
        big_planet,
        far_planets,
        ring_planet,
    ];

    function loop() {
        window.requestAnimationFrame(loop);
        context.clearRect(0, 0, canvas.width, canvas.height);
        let scale = background.width > 0 ? window.innerWidth / background.width : 1;
        for (let object of objects) {
            if (!object.image.width > 0) return;
            object.scale = scale;
            // object.image.onload();
            let speed = object.speed * ((new Date()).getTime() - object.last_draw) ** (1 / 3);
            object.x = object.x - speed;
            if (object.x + object.image.width * object.scale <= 0) {
                object.x = window.innerWidth;
            }
            object.draw();
            object.last_draw = (new Date()).getTime();
        }

    }

    // while (1)
    //     objects.forEach(object => object.draw());
    // setInterval(
    //     () => {
    //         for (let object of objects) {
    //             if (object.image.complete)
    //                 object.draw();
    //         }
    //     }, 1
    // );

    loop()

})
(document);