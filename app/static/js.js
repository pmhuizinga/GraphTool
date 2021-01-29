$(document).ready(function () {
    $('#foodkind').change(function () {

        var foodkind = $('#foodkind').val();

        // Make Ajax Request and expect JSON-encoded data
        $.getJSON(
            '/get_food' + '/' + foodkind,
            function (data) {

                // Remove old options
                $('#food').find('option').remove();

                // Add new items
                $.each(data, function (key, val) {
                    var option_item = '<option value="' + val + '">' + val + '</option>'
                    $('#food').append(option_item);
                });
            }
        );
    });
});



// function add(type) {
//
// //Create an input type dynamically.
// var element = document.createElement("input");
//
// //Assign different attributes to the element.
// element.setAttribute("type", type);
// element.setAttribute("value", type);
// element.setAttribute("name", type);
//
//
// var foo = document.getElementById("fooBar");
//
// //Append the element in page (in span).
// foo.appendChild(element);
// }