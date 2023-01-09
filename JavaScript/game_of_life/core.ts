type t_frame = number[][] 

function new_cell(state: number, resources: number) {
    if (resources === 3 || (resources === 2 && state)) {
        return 1
    } else {
        return 0
    }
}

function new_frame(old_frame: t_frame, resource_distribution: t_frame) {
    return old_frame.map((row, y) => {
        return row.map((state, x) => {
            return new_cell(state, resource_distribution[y][x])
        })
    })
}

function calculate_resources(frame: t_frame) {
    let resource_distribution: t_frame = frame.map(row => new Array(row.length).fill(0))

    for (let y = 0; y < frame.length; y++) {
        const row = frame[y]
        for (let x = 0; x < row.length; x++) {
            if (row[x]) {
                const dy_arr =  (y === 0) ? [frame.length - 1, 0, 1] : 
                                (y === frame.length - 1) ? [-1, 0, 1 - frame.length] :
                                [-1,0,1]
                const dx_arr =  (x === 0) ? [row.length - 1, 0, 1] : 
                                (x === row.length - 1) ? [-1, 0, 1 - row.length] : 
                                [-1,0,1]
                dy_arr.forEach(dy => {
                    dx_arr.forEach(dx => {
                        if (dx || dy) {
                            resource_distribution[y+dy][x+dx] += 1
                        }
                    })
                })
            } 
        }
    }
    return resource_distribution

}

function* frame_generator(init_frame: t_frame, count=Infinity, buffered_frames_size=3): Generator<t_frame> {
    let buffered_frames = new Array<t_frame>(buffered_frames_size)
    let frame = init_frame
    let index = 0

    function loop_control(new_frame: t_frame): boolean {
        let res = false

        for (const element of buffered_frames) {
            if (element && (new_frame.toString() == element.toString())) {
                res = true
                break
            }
        }
        buffered_frames[index++ % buffered_frames_size] = new_frame
        return !res
    } 
    
    while (count-- && loop_control(frame)) {
        yield frame
        const resource_distribution = calculate_resources(frame)
        frame = new_frame(frame, resource_distribution)
    }
}

function render(frame: t_frame, refresh=false) {

    let image_rows = frame.map(row => {
        return row.map(element => {
            return element ? '██' : '  '
        }).join('')
    })
    let image = image_rows.join('\n')
    if (refresh) {console.clear()}
    console.log(image)
}

export { frame_generator, render }