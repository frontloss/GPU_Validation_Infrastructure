function fnToggle() {
    var tab = document.getElementById("tblContainer");
    var rows = tab.rows;
    var cRow = '';
    var nRow = '';
    var rowsLen = rows.length - 1;

    for (var j = 0; j < rowsLen; j++) {
        cRow = document.getElementById(j + 1);
        if (null != cRow) {
            if (cRow.getAttribute("type") != 'null' || cRow.getAttribute("type") != "") {
                if (cRow.getAttribute("type") == "Message")
                    cRow.style.color = "Black";
                else if (cRow.getAttribute("type") == "Verbose")
                    cRow.style.color = "Gray";
                else if (cRow.getAttribute("type") == "Alert")
                    cRow.style.color = "#EFB54A";
                else if (cRow.getAttribute("type") == "Success") {
                    cRow.style.color = "Green";
                    cRow.style.fontWeight = "bold";
                }
                else if (cRow.getAttribute("type") == "Fail") {
                    cRow.style.color = "Red";
                    cRow.style.fontWeight = "bold";
                }
                else if (cRow.getAttribute("type") == "Sporadic") {
                    cRow.style.color = "Magenta";
                    cRow.style.fontWeight = "bold";
                }
                else
                    cRow.style.color = "Black";
            }
            if (cRow.className == "Child") {
                cRow.style.display = "none";
            }

            for (var k = parseInt(cRow.id) ; k < rows.length; k++) {
                nRow = document.getElementById(k + 1);
                if (null != nRow && nRow.className == "Parent")
                    break;

                if ((cRow.getAttribute("error") == "Yes") || (null != nRow && nRow.getAttribute("error") == "Yes")) {
                    if (cRow.className == "Parent") {
                        cRow.style.backgroundColor = "#FF3300";
                        cRow.style.fontWeight = "bold";
                    }
                }
                if ((cRow.getAttribute("type") == "Sporadic") || (null != nRow && nRow.getAttribute("type") == "Sporadic")) {
                    if (cRow.className == "Parent") {
                        cRow.style.color = "Magenta";
                        cRow.style.fontWeight = "bold";
                    }
                }
            }
        }
        else
            rowsLen++;

        rows[j].onclick =
        (
          function () {
              if (this.className == 'Parent') {
                  var expanderAttrib = this.getAttribute("isExpanded");
                  if (null == expanderAttrib) {
                      this.setAttribute("isExpanded", 1);
                      this.cells[0].innerHTML = "&#x25bc;";
                  }
                  else {
                      this.removeAttribute("isExpanded");
                      this.cells[0].innerHTML = "&#9658;";
                  }
                  for (var i = parseInt(this.id) ; i <= rows.length - 1; i++) {
                      nextrow = document.getElementById(i + 1);
                      if (null != nextrow) {
                          if (nextrow.className == 'Child')
                              nextrow.style.display = (nextrow.style.display == '') ? 'none' : '';
                          else if (nextrow.className == 'Parent')
                              break;
                      }
                  }
              }
          }
        )
    }
}

window.onload = function () {
    fnToggle();
}