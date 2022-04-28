document.addEventListener('contextmenu', event => event.preventDefault());

var myChart = new Chart(document.getElementById('mychart'), {
    type: 'doughnut',
    data: {
        labels: ["Efficiency", ""],
        datasets: [{
            label: 'Efficiency',
            data: ["20", "80"],
            backgroundColor: [
                "#a2d6c4",
                "transparent"
            ]
        }]
    },
    options: {
        responsive: true,
        legend: false,
        animation: {
            duration: 0
        }
    }
});

// function addData(data) {
//     alt = 100 - data
//     if (alt < 1) { alt = 0 }
//     vals = [data, alt]
//     myChart.data.datasets = [{
//         label: 'Visitor',
//         data: vals,
//         backgroundColor: [
//             "#a2d6c4",
//             "transparent"
//         ]
//     }]
//     document.getElementById('efficiency').textContent = data + '%'
//     myChart.update(0);
// }
function addData(data) {
    data = Math.round(data)
    colo = perc2color(data)
    alt = 100 - data
    if (alt < 1) { alt = 0 }
    myChart.data.datasets.forEach((dataset) => {
        dataset.data[0] = data;
        dataset.data[1] = alt;
        dataset.backgroundColor[0] = colo
    });
    document.getElementById('efficiency').textContent = data + '%'
    myChart.update(0);
}

function perc2color(perc) {
    perc = perc / 1.5
    var r, g, b = 0;
    if (perc < 50) {
        r = 255;
        g = Math.round(5.1 * perc);
    } else {
        g = 255;
        r = Math.round(510 - 5.10 * perc);
    }
    var h = r * 0x10000 + g * 0x100 + b * 0x1;
    return '#' + ('000000' + h.toString(16)).slice(-6);
}

function openmodal() {
    $('#passwordmodal').modal('show')
}


// setInterval(function() {
//     var data1 = (Math.floor((Math.random() * 100) + 1));
//     addData(data1)

// }, 500);



// $(window).load(function() {
//     // $('#actv').click()
//    
// });
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('actv').click()
});

function updatetarget() {
    const tgt = document.getElementById('ftarget').value
    document.getElementById('rangee').textContent = tgt
}

$('#submit').click(function() {

    const fclient_id = document.getElementById("fclient_id").value;
    const fteam = document.getElementById("fteam").value;
    const fcanspercase = document.getElementById("fcanspercase").value;
    const ftarget = document.getElementById("ftarget").value;

    eel.set_pyconfigs(fclient_id, fteam, fcanspercase, ftarget)
        // alert('settings saved successfully')
    document.getElementById('actv').click()
});

// retrieve settings from python, and save on js
eel.expose(set_jsconfigs);

function set_jsconfigs(client_id, team, canspercase, target, shift) {
    // client title
    document.getElementById('client_id').textContent = client_id.replace(/^\D+/g, '');
    //team
    // document.getElementById("team").textContent = team
    //shift
    document.getElementById("shift").textContent = shift

}

eel.expose(set_eff);

function set_eff(effic) {
    // efficiency
    console.log(effic)
    addData(effic)
}

eel.expose(set_metrics);

function set_metrics(fruitLength, s_cases, avgLength, downtime, fruitCount) {

    //seamed cans
    document.getElementById("fruitLength").textContent = fruitLength

    //seamed cases 
    document.getElementById("s_cases").textContent = s_cases

    //damaged cans
    document.getElementById("avgLength").textContent = avgLength

    //downtime
    document.getElementById("downtime").textContent = downtime

    //downtime
    document.getElementById("fruitCount").textContent = fruitCount

}