let ALL_IMAGES_NUMBER = 0
let CURRENT_IMAGE = ALL_IMAGES_NUMBER

function load_image() {
    let filed = document.getElementById("myFile")
    ALL_IMAGES_NUMBER = filed.files.length
    if (filed.files.length == 0) {
        alert("No files have been chosen.")
        return
    } else {
        let obr = document.getElementById("DICOM-image")
        obr.setAttribute("src", "./assets/img/103.gif")
    }

    hide_3D_image()

    let formData = new FormData();
    const xhttp = new XMLHttpRequest();


    xhttp.open("POST", `http://127.0.0.1:5000/metadata/`, true);
    xhttp.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            console.log("Poszło")
            load_rentgen(CURRENT_IMAGE)
            load_table(CURRENT_IMAGE)
            document.getElementById("numer").innerText = `${CURRENT_IMAGE + 1} \\ ${ALL_IMAGES_NUMBER}`
        }
    }

    ALL_IMAGES_NUMBER = filed.files.length

    for (let ix = 0; ix < filed.files.length; ix++) {
        let file = filed.files[ix]
        if ((!file || 0 === file.length)) {
            alert("Wymagany plik DICOM");
            return
        } else {
            formData.append("file" + ix, file);
        }
    }
    xhttp.send(formData);
}

function load_table(table_number) {
    let req = new XMLHttpRequest();
    req.open('GET', `http://127.0.0.1:5000/opisy/${table_number}/`, true);
    req.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            table_div = document.getElementById("metadata-table");
            table_div.innerHTML = req.responseText;

            df = document.getElementById("opisy")
            df.className = "table table-striped table-sm"
            df.removeAttribute("border")
            thead = df.firstElementChild
            thead.className = "thead-dark"
            tr = thead.firstElementChild
            tr.removeAttribute("style")
            ths = tr.children
            for (i = 0; i < ths.length; i++) {
                let att = ths[i].setAttribute("scope", "col")
            }

            tbody = df.lastElementChild
            trs = tbody.children
            for (i = 0; i < trs.length; i++) {
                trs[i].firstElementChild.setAttribute("scope", "row");
            }


            for (i = 0; i < trs.length; i++) {
                thss = trs[i].children;
                for (j = 0; j < thss.length; j++) {
                    thss[j].setAttribute("style", "word-wrap: break-word;min-width: 160px;max-width: 160px;");
                }
            }
        }
    }
    req.send(null);
}

function load_rentgen(image_number) {
    let obr = document.getElementById("DICOM-image")
    obr.setAttribute("src", `http://127.0.0.1:5000/obrazki/${image_number}/`)
}

function left_arrow_click() {
    if (ALL_IMAGES_NUMBER == 0) {
        return
    }

    CURRENT_IMAGE--
    if (CURRENT_IMAGE < 0) {
        CURRENT_IMAGE = ALL_IMAGES_NUMBER - 1;
    }
    load_rentgen(CURRENT_IMAGE)
    load_table(CURRENT_IMAGE)

    document.getElementById("numer").innerText = `${CURRENT_IMAGE + 1} \\ ${ALL_IMAGES_NUMBER}`
}

function right_arrow_click() {
    if (ALL_IMAGES_NUMBER == 0) {
        return
    }

    CURRENT_IMAGE++
    if (CURRENT_IMAGE >= ALL_IMAGES_NUMBER) {
        CURRENT_IMAGE = 0
    }
    load_rentgen(CURRENT_IMAGE)
    load_table(CURRENT_IMAGE)

    document.getElementById("numer").innerText = `${CURRENT_IMAGE + 1} \\ ${ALL_IMAGES_NUMBER}`
}


function reset_image() {
    console.log("Clicked")
    let req = new XMLHttpRequest();
    req.open('GET', 'http://127.0.0.1:5000/reset/', true);
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        console.log("Obrazki usunięte")
    }
    req.send(null);
}

function hide_3D_image() {
    let elem = document.getElementById("3d-image")
    elem.style.display = "none"
}

function get_3D_image() {
    let elem = document.getElementById("3d-image")
    elem.setAttribute("src", `http://127.0.0.1:5000/obrazki/3D/`);
    elem.setAttribute("class", "upload-image");
    elem.style.display = "block"
}