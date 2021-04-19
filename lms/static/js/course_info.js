
function getNumberOfItemInCart(){
    $.ajax({
        url: '/api/stripe/basket/count_item/',
        success: function(data){
            number_of_item = data['result']['number_of_item']
            if(number_of_item > 0){
                cart_badge = $('#cart_badge').show()
                cart_badge.text(number_of_item)
            }
            else{  
                $('#cart_badge').css('display','none');
            }
        }
    });
}

$(document).ready(function() {
    $('ul.tabs li').click(function() {
        $('ul.tabs li').removeClass('enabled');
        $(this).addClass('enabled');

        var data_class = '.' + $(this).attr('data-class');

        $('.tab').slideUp();
        $(data_class + ':hidden').slideDown();
    });
    var isSafari = !!navigator.userAgent.match(/Version\/[\d\.]+.*Safari/);
    if (isSafari) {
        $('.main-cta').addClass('safari-wrapper');
    }

if ($('.course-price').text() == 'Free')
{
$('#add_to_cart_btn').css('display', 'none');
$('#go_to_cart_btn').css('display', 'none');
$('#buy_now_btn').css('display', 'none');
$('#enroll_now_btn').css('display', '');
}

    
else if($('#already_in_cart').val()== "False")
{
$('#add_to_cart_btn').css('display', '');
$('#go_to_cart_btn').css('display', 'none');
$('#enroll_now_btn').css('display', 'none');
}

else if($('#already_in_cart').val()== "True")
{
$('#add_to_cart_btn').css('display', 'none');
$('#go_to_cart_btn').css('display', '');
$('#enroll_now_btn').css('display', 'none');
}

$("#add_to_cart_btn").click(function(){

    $.ajax({
       type:"POST",
       url: "/api/commerce/v2/add_product/",
       data: JSON.stringify({
       "products":[{"sku":$('#course_sku').val()}],
       csrfmiddlewaretoken: $('#web_csrf_token').val()
     }),
     contentType: "application/json; charset=utf-8",
     success: function(response){
     if (response['status_code'] == 200)
     {
      getNumberOfItemInCart()
      $('#go_to_cart_btn').css('display', '');
      $('#add_to_cart_btn').css('display', 'none');
      $('#buy_now_btn').css('display', '');
      $('#enroll_now_btn').css('display', 'none');
     }
     //else if (response['status_code'] == 500)
     //{
      //alert(response['message']);
     //}

     },
     error: function(data) {
     }
})

});



});
