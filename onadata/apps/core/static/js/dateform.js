(function($) {
    'use strict';
    if ($("#timepicker-example").length) {
      $('#timepicker-example').datetimepicker({
        format: 'LT'
      });
    }
    if ($(".color-picker").length) {
      $('.color-picker').asColorPicker();
    }
    if ($(".datepicker").length) {
      $('.datepicker').datepicker({
        enableOnReadonly: true,
        todayHighlight: true,
        autoclose: true,
      });
    }
    if ($("#inline-datepicker").length) {
      $('#inline-datepicker').datepicker({
        enableOnReadonly: true,
        todayHighlight: true,
      });
    }
    if ($(".datepicker-autoclose").length) {
      $('.datepicker-autoclose').datepicker({
        autoclose: true
      });
    }
    if ($('input[name="date-range"]').length) {
      $('input[name="date-range"]').daterangepicker();
    }
    if ($('input[name="date-time-range"]').length) {
      $('input[name="date-time-range"]').daterangepicker({
        timePicker: true,
        timePickerIncrement: 30,
        locale: {
          format: 'MM/DD/YYYY h:mm A'
        }
      });
    };
    
    

    function uploadFile() {
      $('[data-behaviour="custom-upload-input"]').on('change', updateButton);
      function updateButton(e) {
        var inputValue = $(e.currentTarget).val().split( '\\' ).pop();
        $('[data-element="custom-upload-button"]').text(inputValue)
        e.preventDefault;
      };
    };
    uploadFile();

    function checkbox(){
      $(".select-all").change(function () {
        $(this).closest('.card').find('.checkbox input').prop('checked', $(this).prop("checked"));
      });
    
      $(".checkbox input").change(function() {
          var checkboxes = $(this).closest('.checkbox').find('input');
          var checkedboxes = checkboxes.filter(':checked');
      
          if(checkboxes.length === checkedboxes.length) {
          $(this).closest('.card-header').find('.select-all').prop('checked', true);
          } else {
            $(this).closest('.card-header').find('.select-all').prop('checked', false);
            
          }
      });
    };
    checkbox();
   
    $('.select2').select2();
    
  })(jQuery);

//   $(".select-all").change(function () {
//     $(".checkbox input").prop('checked', $(this).prop("checked"));
// });

// $(".checkbox input").change(function() {
//     var checkboxes = $('.checkbox input');
//     var checkedboxes = checkboxes.filter(':checked');

//     if(checkboxes.length === checkedboxes.length) {
//      $('.select-all').prop('checked', true);
//     } else {
//     $('.select-all').prop('checked', false);
//     }
// });
