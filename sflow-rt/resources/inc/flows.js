$(document).ready(function() {
    $("#flows tbody tr")
       .filter(function() {
         return $(this).hasClass("even") || $(this).hasClass("odd")
       })
       .hover(
         function() { $(this).addClass("dynhoveron"); },
         function() { $(this).removeClass("dynhoveron"); }
       )
       .click(
         function() { 
           var cells = $(this).find("td");
           var metric = cells[0];
           document.location = "../metric/ALL/" + metric.innerHTML + "/html"; }
       )
})
