$(document).ready(function() {

    var doc_ols = document.getElementsByTagName("ol");
    for ( i=0; i<doc_ols.length; i++) {
        var ol_start = doc_ols[i].getAttribute("start") - 1;
        doc_ols[i].setAttribute("style", "counter-reset:ol " + ol_start + ";");
    };

    moment.locale('zh-cn');
    $('.timestamp').each(function(){
        var timestamp = $(this).html();
        var daysBefore = moment(timestamp, "YYYY-MM-DD hh:mm:ss").fromNow()
        $(this).html(daysBefore);
    });
    $('.archivetime').each(function(){
        var timestamp = $(this).find('input').val();
        $(this).html(moment.unix(timestamp).format('LL'));
    });
});