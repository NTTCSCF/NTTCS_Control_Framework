function doSearch()

        {
            const tableReg = document.getElementById('datos');
            const searchText = document.getElementById('busqueda').value.toLowerCase();
            let total = 0;

            // Recorremos todas las filas con contenido de la tabla
            for (let i = 1; i < tableReg.rows.length; i++) {
                // Si el td tiene la clase "noSearch" no se busca en su cntenido
                if (tableReg.rows[i].classList.contains("noSearch")) {
                    continue;
                }
                let found = false;
                const cellsOfRow = tableReg.rows[i].getElementsByTagName('td');
                // Recorremos todas las celdas
                for (let j = 0; j < cellsOfRow.length && !found; j++) {
                    const compareWith = cellsOfRow[j].innerHTML.toLowerCase();
                    // Buscamos el texto en el contenido de la celda
                    if (searchText.length == 0 || compareWith.indexOf(searchText) > -1) {
                        found = true;
                        total++;
                    }
                }
                if (found) {
                    tableReg.rows[i].style.display = '';
                } else {
                    // si no ha encontrado ninguna coincidencia, esconde la
                    // fila de la tabla
                    tableReg.rows[i].style.display = 'none';
                }
            }

            // mostramos las coincidencias
            const lastTR=tableReg.rows[tableReg.rows.length-1];
            const td=lastTR.querySelector("td");
            lastTR.classList.remove("hide", "red");
            if (searchText == "") {
                lastTR.classList.add("hide");
            }
        }



//PARA DATA TABLES DOMINIOS

//  CONTROLES NTTCS

let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnsDefs: [
        { orderable: false},
        { searchable: true},
    ],
    pageLength: 100,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listControlesNttcs();

    dataTable = $("#datatable_controlesnttcs").dataTable(dataTableOptions);
    dataTableIsInitialized = true;
};


const listControlesNttcs = async () => {

    try {
        const response=await fetch('http://127.0.0.1:8000/MantenimientoControlesNTTCS/list_controlesnttcs');
        const data = await response.json();


        let content = ``;
        let content2 = ``;
        data.controles_nttcs.forEach((controles_nttcs,index) => {


            content += `
                 <tr>
                    <form method="post">
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.domain}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.selected_y_n_field}"></td>
                        <td><input class="inputTabas" style="width:150px;" rows="5" type="text" value="${controles_nttcs.control}"></td>
                        <td><input type="text" class="inputTabas" style="width:150px;" rows="5" value="${controles_nttcs.control_description}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.relative_control_weighting}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.function_grouping}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.assesed_result}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.numeric_result}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.weighted_numeric_result}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.assessment_comments}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.relative_result_by_function}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.relative_result_by_domain}"></td>
                        <td class="botonesTabla">
                            <button class="btn btn-warning btn-sm" title="Editar" id="modificar" name="modificar">
                                <i class="bi bi-pencil-square"></i>
                            </button>
                            <button class="btn btn-danger btn-sm" title="Borrar" id="eliminar" name="eliminar">
                                <i class="bi bi-trash3"></i>
                            </button>
                        </td>
                    </form>
                 </tr>
            `;

        });

        tableControlesNttcs.innerHTML = content;

    } catch (ex) {
        alert(ex);
    }
};

// INICIALIZACION DEL DATATABLE
window.addEventListener("load", async () => {
    await initDataTable();
});




// INICIALIZACION DEL DATATABLE
//window.addEventListener("load", async () => {
   // await initDataTable();
//});