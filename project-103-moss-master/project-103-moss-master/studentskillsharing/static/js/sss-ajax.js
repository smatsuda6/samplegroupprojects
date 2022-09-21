$("#connect").on('click', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers').html(data.followers)
                    $('#connect').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#connect').html('Unfollow');
               } else {
                    $('#followers').html(data.followers)
                    $('#connect').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#connect').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation1', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers1').html(data.followers)
                    $('#recommendation1').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation1').html('Unfollow');
               } else {
                    $('#followers1').html(data.followers)
                    $('#recommendation1').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation1').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation2', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers2').html(data.followers)
                    $('#recommendation2').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation2').html('Unfollow');
               } else {
                    $('#followers2').html(data.followers)
                    $('#recommendation2').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation2').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation3', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers3').html(data.followers)
                    $('#recommendation3').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation3').html('Unfollow');
               } else {
                    $('#followers3').html(data.followers)
                    $('#recommendation3').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation3').html('Follow');
               }
           });
});


$(document).on('click', '#recommendation4', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers4').html(data.followers)
                    $('#recommendation4').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation4').html('Unfollow');
               } else {
                    $('#followers4').html(data.followers)
                    $('#recommendation4').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation4').html('Follow');
               }
           });
});


$(document).on('click', '#recommendation5', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers5').html(data.followers)
                    $('#recommendation5').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation5').html('Unfollow');
               } else {
                    $('#followers5').html(data.followers)
                    $('#recommendation5').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation5').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation6', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers6').html(data.followers)
                    $('#recommendation6').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation6').html('Unfollow');
               } else {
                    $('#followers6').html(data.followers)
                    $('#recommendation6').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation6').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation7', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers7').html(data.followers)
                    $('#recommendation7').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation7').html('Unfollow');
               } else {
                    $('#followers7').html(data.followers)
                    $('#recommendation7').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation7').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation8', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers8').html(data.followers)
                    $('#recommendation8').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation8').html('Unfollow');
               } else {
                    $('#followers8').html(data.followers)
                    $('#recommendation8').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation8').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation9', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers9').html(data.followers)
                    $('#recommendation9').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation9').html('Unfollow');
               } else {
                    $('#followers9').html(data.followers)
                    $('#recommendation9').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation9').html('Follow');
               }
           });
});

$(document).on('click', '#recommendation10', function(){
    var profileid;
    profileid = $(this).attr("data-profileid");
     $.get('/studentskillsharing/connect_with_profile/', {'profile_id': profileid}, function(data){
               if(data.user_follow_status){
                    $('#followers10').html(data.followers)
                    $('#recommendation10').removeClass('btn btn-outline-success').addClass('btn btn-success');
                    $('#recommendation10').html('Unfollow');
               } else {
                    $('#followers10').html(data.followers)
                    $('#recommendation10').removeClass('btn btn-success').addClass('btn btn-outline-success');
                    $('#recommendation10').html('Follow');
               }
           });
});