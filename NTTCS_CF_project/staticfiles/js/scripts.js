function doSearch(){
            const tableReg = document.getElementById('data');
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

$('#busqueda').keyup(function(e){
     consulta = $("#busqueda").val();
     $.ajax({
         data: {'busca': consulta},
         url: '/listadoControles/',
         type: 'get',
         success : function(data) {
                 console.log(data[0].nombre);
     },
     error : function(message) {
             console.log(message);
          }
     });
});


//PARA DATA TABLES NTTCS
/**
 $(document).ready(function () {
    //listadoControles();
    $('#tabla_controlesnttcs'). DataTable({
        "serverSide":true,
        "processing":true,
        "ajax":function(data, callback, settings) {
            $.get('/listadoControles/',{
                limite: data.length,
                inicio: data.start
                }, function(res) {
                console.log(res)
                callback({
                    recordsTotal: res.length,
                    recordsFiltered: res.length,
                    data: res.object
                    });
                },
            );
        },

        columns:[
            { data: "domain" },
            { data: "selected_y_n_field" },
            { data: "control" },
            { data: "id" },
            { data: "control_description" },
            { data: "relative_control_weighting" },
            { data: "function_grouping" },
            { data: "assesed_result" },
            { data: "numeric_result" },
            { data: "weighted_numeric_result" },
            { data: "assessment_comments" },
            { data: "relative_result_by_function" },
            { data: "relative_result_by_domain" }
            ]
    });
});**/

function listadoControles() {
    console.log("hola");
    $.ajax({
        url: "/listadoControles/",
        type: "get",
        dataType: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_controlesnttcs')) {
                $('#tabla_controlesnttcs'). DataTable().destroy();
            }
            $('#tabla_controlesnttcs tbody').html("");
            let inputs = `<tr>
                <form method="post">
                    {% csrf_token %}
                    <td><input class="inputTabas" style="width:100px;" type="text" name="domain" placeholder="Insert domain" autocomplete="false" ></td>
                    <td><input class="inputTabas" type="text" name="selected_y_n_field" placeholder="Insert selected_y_n_field" autocomplete="false" ></td>
                    <td><input class="inputTabas" type="text" style="width:150px;" name="control" placeholder="Insert control" autocomplete="false"></td>
                    <td><input class="inputTabas" type="text" name="id" placeholder="Insert id" autocomplete="false" ></td>
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
                        <button class="btn btn-success btn-sm" title="Guardar" id="insertar" name="insertar" >
                            <i class="bi bi-check2-square"></i>
                        </button>
                    </td>
                </form>
            </tr>`;
            $('#tabla_controlesnttcs tbody').append(inputs);
            for (let i = 0; i < response.length; i++) {
                let fila = `<tr>
                <form method="post">
                    {% csrf_token %}
                    <td><input class="inputTabas" type="text" value="` + response[i]["domain"] + `" name="domain" ></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["selected_y_n_field"] + `" name="selected_y_n_field" ></td>
                    <td><textarea class="inputTabas" style="width:150px;" rows="5" type="text" value="` + response[i]["control"] + `" name="control" >` + response[i]["control"] + `</textarea></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["id"] + `" name="id" ></td>
                    <td><textarea class="inputTabas" style="width:150px;" rows="5" type="text" value="` + response[i]["control_description"] + `" name="control_description" >` + response[i]["control_description"] + `</textarea></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["relative_control_weighting"] + `" name="relative_control_weighting"></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["function_grouping"] + `" name="function_grouping" ></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["assesed_result"] + `" name="assesed_result" ></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["numeric_result"] + `" name="numeric_result" ></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["weighted_numeric_result"] + `" name="weighted_numeric_result"></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["assessment_comments"] + `" name="assessment_comments" ></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["relative_result_by_function"] + `" name="relative_result_by_function" ></td>
                    <td><input class="inputTabas" type="text" value="` + response[i]["relative_result_by_domain"] + `" name="relative_result_by_domain" ></td>
                    <td class="botonesTabla">
                        <button class="btn btn-warning btn-sm" title="Editar" id="modificar" name="modificar">
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button class="btn btn-danger btn-sm" title="Borrar" id="eliminar" name="eliminar">
                            <i class="bi bi-trash3"></i>
                        </button>
                    </td>
                </form>
            </tr>`;
                $('#tabla_controlesnttcs tbody').append(fila);
            }
            $('#tabla_controlesnttcs'). DataTable({
                "Language": {
                    "decimal": "",
                    "empty Table": "No hay información",
                    "info": "Mostrando _START_ a_END_ de _TOTAL_ Entradas",
                    "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                    "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                    "infoPostFix": "",
                    "thousands": ",",
                    "LengthMenu": "Mostrar _MENU_ Entradas",
                    "LoadingRecords": "Cargando...",
                    "processing": "Procesando...",
                    "search": "Buscar:",
                    "zeroRecords": "Sin resultados encontrados",
                    "paginate": {
                        "first": "Primero",
                        "Last": "Ultimo",
                        "next": "Siguiente",
                        "previous": "Anterior"
                    },
                },
            });
            console.log("salida")
        }

    });

}

//DATATABLES PRACTICAS EN DOMINIOS2

