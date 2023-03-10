var canvases = undefined;

function progressive_draw(image) {
    last = false;
    for (i in image) {
        if (i == Object.keys(image).length - 1) {
            last = true;
        }
        pixel = image[i];
        wipe(ctx);
        setTimeout(
            draw_pixel.bind(null, pixel, ctx, last),
            pixel.order_number*100);
    }
}

function draw_pixel(pixel, context, last) {
    context.fillStyle = pixel.color;
    context.fillRect(pixel.row_number, pixel.col_number, 1, 1);
    if (last) {
        setup();
    }
}

function draw_images(images) {
    console.log(images);
    canvases = document.querySelectorAll("[id=pixelCanvas]");
    canvases.forEach(canvas => {
        canvas.setAttribute('data-drawn', false);
    });
    document.post_images = images;
    document.canvases = canvases;
    document.addEventListener('scroll', draw_if_visible);
    document.addEventListener('DOMContentLoaded', draw_if_visible);
}

function draw_if_visible(event) {
    images = event.currentTarget.post_images;
    canvases = event.currentTarget.canvases;
    canvas_i = 0
    for (i in images) {
        if (images[i].data == undefined) {
            image = images[i];
        } else {
            image = images[i].data;
        }
        canvas = canvases[canvas_i];
        var top = $(window).scrollTop();
        var bottom = top + $(window).height();
        var canvas_top = $(canvas).offset().top;
        var canvas_bottom = canvas_top + $(canvas).height();

        if ((canvas_top >= top) && (canvas_bottom <= bottom) && canvas.getAttribute("data-drawn") === 'false') {
            canvas.setAttribute("data-drawn", 'true');
            ctx = canvas.getContext("2d");
            progressive_draw(image);
        } else if (((canvas_top > bottom) || (canvas_bottom < top)) && canvas.getAttribute("data-drawn") === 'true') {
            canvas.setAttribute("data-drawn", 'false');
            ctx = canvas.getContext("2d");
            prev = ctx.fillStyle;
            wipe(ctx);
            ctx.fillStyle = prev;
        }
        canvas_i++;
    }
}

function wipe(context) {
    context.fillStyle = "white";
    context.fillRect(0, 0, 32, 32);
}

function invoke_error(error) {
    error.json().then(
        function (data) {
            console.log(data);
            window.alert(data.message);
        }
    )
}
