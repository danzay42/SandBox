function new_cell(state, resources) {
    if (resources === 3 || (resources === 2 && state)) {
        return 1;
    }
    else {
        return 0;
    }
}
function new_frame(old_frame, resource_distribution) {
    return old_frame.map((row, y) => {
        return row.map((state, x) => {
            return new_cell(state, resource_distribution[y][x]);
        });
    });
}
function calculate_resources(frame) {
    let resource_distribution = frame.map(row => new Array(row.length).fill(0));
    for (let y = 0; y < frame.length; y++) {
        const row = frame[y];
        for (let x = 0; x < row.length; x++) {
            if (row[x]) {
                const dy_arr = (y === 0) ? [frame.length - 1, 0, 1] :
                    (y === frame.length - 1) ? [-1, 0, 1 - frame.length] :
                        [-1, 0, 1];
                const dx_arr = (x === 0) ? [row.length - 1, 0, 1] :
                    (x === row.length - 1) ? [-1, 0, 1 - row.length] :
                        [-1, 0, 1];
                dy_arr.forEach(dy => {
                    dx_arr.forEach(dx => {
                        if (dx || dy) {
                            resource_distribution[y + dy][x + dx] += 1;
                        }
                    });
                });
            }
        }
    }
    return resource_distribution;
}
function* frame_generator(init_frame, count = Infinity, buffered_frames_size = 3) {
    let buffered_frames = new Array(buffered_frames_size);
    let frame = init_frame;
    let index = 0;
    function loop_control(new_frame) {
        let res = false;
        for (const element of buffered_frames) {
            if (element && (new_frame.toString() == element.toString())) {
                res = true;
                break;
            }
        }
        buffered_frames[index++ % buffered_frames_size] = new_frame;
        return !res;
    }
    while (count-- && loop_control(frame)) {
        yield frame;
        const resource_distribution = calculate_resources(frame);
        frame = new_frame(frame, resource_distribution);
    }
}
function render(frame, refresh = false) {
    let image_rows = frame.map(row => {
        return row.map(element => {
            return element ? '██' : '  ';
        }).join('');
    });
    let image = image_rows.join('\n');
    if (refresh) {
        console.clear();
    }
    console.log(image);
}
export { frame_generator, render };
