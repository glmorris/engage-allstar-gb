$(document).ready(function(){
  $('#languageSelector').on('change', function(){
    window.location = '/change-language?lang=' + $(this).val();
  });
});