const spin1 = document.getElementById("randSpin1");
const spin2 = document.getElementById("randSpin2");
const spin3 = document.getElementById("randSpin3");
const spin4 = document.getElementById("randSpin4");
const spin5 = document.getElementById("randSpin5");


function randomize(spin)
{
    var spinVal, transVal, marginVal;

    // Random Rotation
    spinVal = Math.floor(Math.random() * 30) + 1;
    if((Math.floor(Math.random() * 2) + 1) == 1) {spinVal *= -1}
    transVal = "rotate(" + spinVal + "deg)";

    var marginVal = Math.floor(Math.random() * 5) + 3;

    // Spin and move spin1
    spin.style.transform = transVal;
    spin.style.margin = marginVal + "%";
}

randomize(spin1);
randomize(spin2);
randomize(spin3);
randomize(spin4);
randomize(spin5);
