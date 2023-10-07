var colorContainer = [];
const blue = [
    "#03effc",
    "#03d1dd",
    "#02b3bd",
    "#02959e",
    "#02777e",
    "#015a5f",
    "#013c3f",
    "#001e20",
    "#001C1E",
    "#000E0F"];
const yellow = [
    "#ffb700",
    "#dfa000",
    "#bf8900",
    "#9f7200",
    "#805b00",
    "#604500",
    "#402e00",
    "#201700",
    "#201700",
    "#080600"];
const pink = [
    "#ff002d",
    "#df0027",
    "#bf0022",
    "#9f001c",
    "#800016",
    "#600011",
    "#40000b",
    "#200006",
    "#140004",
    "#080002"
];
const green = [
    "#00ff33",
    "#00df2d",
    "#00bf26",
    "#009f20",
    "#00801a",
    "#006013",
    "#00400d",
    "#002006",
    "#001404",
    "#000802",
]
const lemon = [
    "#b3ff08",
    "#9ddf07",
    "#86bf06",
    "#709f05",
    "#598004",
    "#436003",
    "#2d4002",
    "#162001",
    "#223002",
    "#080C00",
]
const colors = [blue, yellow, pink, green, lemon];



for (let i = 0; i < 10; i++) {
    document.body.style.setProperty("--c" + i, colors[4][i]);
}

document.body.style.setProperty("--wx", window.innerWidth);
document.body.style.setProperty("--wy", window.innerHeight);

window.addEventListener('mousemove', function (e) {
    document.body.style.setProperty("--px", e.clientX);
    document.body.style.setProperty("--py", e.clientY);
})
window.addEventListener('scroll', function (e) {
    document.body.style.setProperty("--sc", this.window.scrollY);
})