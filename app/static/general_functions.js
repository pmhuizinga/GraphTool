function addNewPropRow(source_target) {
    var presentRows = $("#new_" + source_target + "_property > div");
    var newRowId = presentRows.length + 1;
    $("#new_" + source_target + "_property").append('<div class="menu_row">' +
        '<div class="menu_item"><input type="text" name="' + source_target + '_property_name' + newRowId + '" placeholder="property type"/></div>' +
        '<div class="menu_item"><input type="text" name="' + source_target + '_property_value' + newRowId + '" placeholder="property value"/></div>' +
        '</div>');
}

function addCurrentDate(){
    n =  new Date();
    y = n.getFullYear();
    m = n.getMonth() + 1;
    d = n.getDate();
    datestring = y + "-" + m + "-" + d;

    return datestring
}