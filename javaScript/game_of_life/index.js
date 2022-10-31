import { readFileSync } from "fs"
import { frame_generator, render } from "./core.js";

main()

async function main() {

    let obj = JSON.parse(readFileSync("../../patterns_examples.json", 'utf8'))
    let init_frame = obj.Oscillators["Penta-decathlon"]
    // let init_frame = obj.Oscillators["Pulsar"]
    // let init_frame = obj.Spaceships.Glider
    // let init_frame = obj.Spaceships.HWSS

    for await (const frame of frame_generator(init_frame, 1e4)) {
        render(frame)
        // await new Promise(r => setTimeout(r, 200))
    }    
}
