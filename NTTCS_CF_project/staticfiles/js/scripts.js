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


//columna de opciones
const dataTableOptions = {
    columnsDefs: [
        { orderable: true},
        { searchable: true},
    ],
    pageLength: 100,
    destroy: true
};

//inicializacion del datatable
const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listDominios();

    dataTable = $("#datatable_controlesnttcs").dataTable(dataTableOptions);
    dataTableIsInitialized = true;
};

//controls list
const listControlesNttcs = async () => {

    try {
        const response=await fetch('http://127.0.0.1:8000/MantenimientoControlesNTTCS/list_controlesnttcs');
        const data = await response.json();


        let content = `
            <tr>
                <form method="post">

                    <input type="hidden" value="´{% csrf_token %}"
                    <td><input class="inputTabas" style="width:100px;" type="text" name="domain" placeholder="Insert domain" autocomplete="false" ></td>
                    <td><input class="inputTabas" type="text" name="selected_y_n_field" placeholder="Insert selected_y_n_field" autocomplete="false" ></td>
                    <td><input class="inputTabas" type="text" style="width:150px;" name="control" placeholder="Insert control" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" style="width:150px;" name="control_description" placeholder="insert Description" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="relative_control_weighting" placeholder="insert relative_control_weighting" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="function_grouping" placeholder="insert function_grouping" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="assesed_result" placeholder="insert assesed_result" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="numeric_result" placeholder="insert numeric_result" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="weighted_numeric_result" placeholder="insert weighted_numeric_result" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="assessment_comments" placeholder="insert assessment_comments" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="relative_result_by_function" placeholder="insert relative_result_by_function" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="relative_result_by_domain" placeholder="insert relative_result_by_domain" autocomplete="false"></td>
                    <td class="botonesTabla">
                        <button class="btn btn-success btn-sm" title="Guardar" id="insertar" name="insertar">
                            <i class="bi bi-check2-square"></i>
                        </button>
                    </td>
                </form>
            </tr>
        `;

        data.controles_nttcs.forEach((controles_nttcs,index) => {

            content += `
                 <tr>
                    <form method="post">
                        <py-script>{% csrf_token %}</py-script>
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
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.relative_result_by_function.toFixed(2)}"></td>
                        <td><input type="text" class="inputTabas" value="${controles_nttcs.relative_result_by_domain.toFixed(2)}"></td>
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
*/

new DataTable('#datatable_dominios', {
    paging: false,
    scrollCollapse: true,
    scrollY: '200px'
});