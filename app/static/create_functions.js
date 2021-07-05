// asynchronic jquery function for retrieving inputbox data dynamically

$(document).ready(
    function () {
        var collection;
        $('#source_collection_name').change(function () {
                collection = $('#source_collection_name').val();
                // console.log(collection)
                // Make Ajax Request and expect JSON-encoded data
                // get node id's
                $.getJSON(
                    '/get_collection_ids/node/' + collection,
                    function (id_data) {
                        var node_id = (id_data);
                        // console.log(node_id)
                        autocomplete(document.getElementById("source_collection_id"), node_id);
                    });
                // get node fields
                $.getJSON(
                    '/get_collection_fieldnames/node/' + collection,
                    function (field_data) {
                        var field_name = (field_data);
                        // console.log(field_name)
                        document.getElementById("source_fields").innerHTML = "";
                        $.each(field_data, function (k, v) {
                            document.getElementById('source_fields').innerHTML += '<div class="menu_row">' +
                                '<div class="menu_item">' + v + '</div>' +
                                '<div class="menu_item"><input type="text" name="source_' + v + '"></div>' +
                                '</div>';
                            console.log('finish adding node types')
                        });
                    });
            }
        )
    });

$(document).ready(
    function () {
        var collection;
        $('#source_collection_id').change(function () {
                collection = $('#source_collection_name').val();
                record_id = $('#source_collection_id').val();
                console.log('source collection id')
                console.log(collection)
                console.log(record_id)
                // Make Ajax Request and expect JSON-encoded data
                // get node id's
                // get node fields
                $.getJSON(
                    '/get_collection_record/node/' + collection + '/' + record_id,
                    function (field_data) {
                        var field_name = (field_data);
                        // console.log(field_name)
                        document.getElementById("source_fields").innerHTML = "";
                        $.each(field_data, function (k, v) {
                            document.getElementById('source_fields').innerHTML += '<div class="menu_row">' +
                                '<div class="menu_item">' + k + '</div>' +
                                '<div  class="menu_item">' +
                                '<input type="text" name="source_' + k + '" value="' + v + '">' +
                                '</div>' +
                                '</div>';
                        });
                    });
                create_graph('node', record_id)
            }
        )
    });

$(document).ready(
    function () {
        var collection;
        $('#edge_value').change(function () {
                // collection = $('#source_collection_name').val();
                record_id = $('#edge_value').val();
                create_graph('edge', record_id)

            // $.getJSON(
            //         '/get_collection_fieldnames/edge/' + collection,
            //         function (field_data) {
            //             var field_name = (field_data);
            //             console.log(field_name)
            //             document.getElementById("edge_fields").innerHTML = "";
            //             $.each(field_data, function (k, v) {
            //                 document.getElementById('edge_fields').innerHTML += '<div class="menu_row">' +
            //                     '<div class="menu_item">' + v + '</div>' +
            //                     '<div class="menu_item"><input type="text" name="edge' + v + '"></div>' +
            //                     '</div>';
            //                 console.log('finish adding node types')
            //             });
            //         });

            }
        )
    });


$(document).ready(
    function () {
        var collection;
        $('#target_collection_name').change(function () {
                collection = $('#target_collection_name').val();
                console.log(collection)
                // Make Ajax Request and expect JSON-encoded data
                // get node id's
                $.getJSON(
                    '/get_collection_ids/node/' + collection,
                    function (id_data) {
                        var node_id = (id_data);
                        console.log(node_id)
                        autocomplete(document.getElementById("target_collection_id"), node_id);
                    });
                // get node fields
                $.getJSON(
                    '/get_collection_fieldnames/node/' + collection,
                    function (field_data) {
                        var field_name = (field_data);
                        console.log(field_name)
                        document.getElementById("target_fields").innerHTML = "";
                        $.each(field_data, function (k, v) {
                            document.getElementById('target_fields').innerHTML += '<div class="menu_row">' +
                                '<div class="menu_item">' + v + '</div>' +
                                '<div class="menu_item"><input type="text" name="target_' + v + '"></div>' +
                                '</div>';
                            console.log('finish adding node types')
                        });
                    });
            }
        )
    });

$(document).ready(
    function () {
        var collection;
        $('#target_collection_id').change(function () {
                collection = $('#target_collection_name').val();
                record_id = $('#target_collection_id').val();
                console.log(collection)
                console.log(record_id)
                // Make Ajax Request and expect JSON-encoded data
                // get node id's
                // get node fields
                $.getJSON(
                    '/get_collection_record/node/' + collection + '/' + record_id,
                    function (field_data) {
                        var field_name = (field_data);
                        console.log(field_name)
                        document.getElementById("target_fields").innerHTML = "";
                        $.each(field_data, function (k, v) {
                            document.getElementById('target_fields').innerHTML += '<div class="menu_row">' +
                                '<div class="menu_item">' + k + '</div>' +
                                '<div  class="menu_item">' +
                                '<input type="text" name="target_' + k + '" value="' + v + '">' +
                                '</div>' +
                                '</div>';
                        });
                    });
                test()
            }
        )
    });

$(".source_node_collapse").click(function () {

    $header = $(this);
    //getting the next element
    $content = $header.next();
    //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
    $content.slideToggle(500, function () {
        //execute this after slideToggle is done
        //change text of header based on visibility of content div
        $header.text(function () {
            //change text based on condition
            return $content.is(":visible") ? "Collapse" : "Expand";
        });
    });

});

$(".target_node_collapse").click(function () {

    $header = $(this);
    //getting the next element
    $content = $header.next();
    //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
    $content.slideToggle(500, function () {
        //execute this after slideToggle is done
        //change text of header based on visibility of content div
        $header.text(function () {
            //change text based on condition
            return $content.is(":visible") ? "Collapse" : "Expand";
        });
    });

});

$(".edge_collapse").click(function () {

    $header = $(this);
    //getting the next element
    $content = $header.next();
    //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
    $content.slideToggle(500, function () {
        //execute this after slideToggle is done
        //change text of header based on visibility of content div
        $header.text(function () {
            //change text based on condition
            return $content.is(":visible") ? "Collapse" : "Expand";
        });
    });

});


function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function (e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function (e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {

        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        console.log(x[currentFocus])
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
        except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

$.getJSON(
    '/get_collections/node',
    function (id_data) {
        var node_type = (id_data);
        autocomplete(document.getElementById("source_collection_name"), node_type);
        autocomplete(document.getElementById("target_collection_name"), node_type);
    });

$.getJSON(
    '/get_collections/edge',
    function (id_data) {
        var node_type = (id_data);
        autocomplete(document.getElementById("edge_value"), node_type);
    });


