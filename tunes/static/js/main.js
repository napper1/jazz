$(document).ready(function () {

    //$(".add-song-form").submit(function (e) {
    //    e.preventDefault();
    //    var form = $(this).serialize();
    //    var posting = jQuery.post('/music/api-add-song/', form);
    //    posting.done(function (data) {
    //        if (data.response === true) {
    //            var song_row = "<tr><td>" + data.title + "</td> +" +
    //                "<td>" + "<a href=" + data.link + "class='blue-text text-darken-4 target='_blank'> <i class='small material-icons'>queue_music</i> </a>" + "</td>" +
    //                "<td>" + data.tab_link + "</td>" +
    //                "<td><a href='' class='remove-song' data-song-id=" + data.song_id + ">" +
    //                "<i class='material-icons'>delete</i></a></td>" +
    //                "</tr>";
    //            $(".song-table").prepend(song_row);
    //            Materialize.toast('Song added!', 2000)
    //        }
    //    });
    //});

    $(".remove-song").on("click", function () {
        var song_id = $(this).data("song-id");
        var song_row = $(this).parent().parent();
        var data = {song_id: song_id};
        var posting = jQuery.post('/music/api-remove-song/', data);
        posting.done(function (data) {
            if (data.response === true) {
                song_row.hide();
                Materialize.toast('Song removed!', 2000);
            }
        })
    });

});