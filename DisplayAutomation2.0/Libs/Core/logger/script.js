function toggleDebugLogs() {
    var btn = document.getElementById('debugBtn');
    var dr = document.getElementsByClassName("dr");
    var dc = document.getElementsByClassName("dc");
    var drow = document.getElementsByClassName("drow");
    var is_debug_on = true, i = 0;

    if (btn.innerHTML === "Turn ON Debug Mode") {
        btn.innerHTML = "Turn OFF Debug Mode";
    } else {
        btn.innerHTML = "Turn ON Debug Mode";
        is_debug_on = false;
    }
    for (i = 0; i < dr.length; i++) {
        if (is_debug_on) {
            dr[i].style.display = "table-row";
        } else {
            dr[i].style.display = "none";
        }
    }
    for (i = 0; i < dc.length; i++) {
        if (is_debug_on) {
            dc[i].style.display = "table-cell";
        } else {
            dc[i].style.display = "none";
        }
    }
    for (i = 0; i < drow.length; i++) {
        if (is_debug_on) {
            drow[i].style.display = "table-row";
        } else {
            drow[i].style.display = "none";
        }
    }
}

function toggleVisibility(id, c) {
    var e = document.getElementById(id);

    if (e.style.display === "none") {
        e.style.display = c;
    } else {
        e.style.display = "none";
    }
}

function toggleStepView(step_index) {
    var d = document.getElementsByClassName('sl' + step_index);
    var i = 0;
    var display = 'table-row';

    for (i = 0; i < d.length; i++) {
        if(!d[i].classList.contains('dr')){
            if(d[i].style.display === "table-row")
                display = "none";
            break;
        }
    }

    for (i = 0; i < d.length; i++) {
        if(d[i].classList.contains('dr'))
            continue;
        d[i].style.display = display;
    }
}
