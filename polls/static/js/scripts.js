// Functions
function recountEducItems(numClicked) {
  $('#signup-educ').children().length;

  let items = $('#signup-educ').children();

  let i = 1;

  for (let item of items) {
    if (i < numClicked) {
      i++;
      continue;
    }

    let info = $(item).children()[0];

    if ($(info).find())

    $(info).find('.signup-educ-item-num span').css({
      'transform': 'translateX(30px)',
      'opacity': '0',
      'visibility': 'hidden'
    });

    let m = i;
    setTimeout(() => {

      $(info).find('.signup-educ-item-num').prepend('<span class="signup-educ-item-num-hidden">#' + m + '</span>');
      $(info).find('.signup-educ-item-num span')[1].remove();

      setTimeout(() => {
        $(info).find('.signup-educ-item-num span').css({
          'visibility': 'visible',
          'opacity': '1',
          'transform': 'translateX(0)'
        });
      }, 20);
    }, 400);

    i++;
  }

  i = 1;

  for (let item of items) {
    let inputs = $(item).children('.inputline');
    //console.log($(inputs[0]).find('label').attr('for'))
    $(inputs[0]).find('label').attr('for', 'id_form-' + (i - 1) +'-university');
    $(inputs[0]).find('input').attr('id', 'id_form-' + (i - 1) +'-university');
    $(inputs[0]).find('input').attr('name', 'form-' + (i - 1) +'-university');
    $(inputs[1]).find('label').attr('for', 'id_form-' + (i - 1) +'-degree');
    $(inputs[1]).find('select').attr('id', 'id_form-' + (i - 1) +'-degree');
    $(inputs[1]).find('select').attr('name', 'form-' + (i - 1) +'-degree');
    $(inputs[2]).find('label').attr('for', 'id_form-' + (i - 1) +'-educ_start');
    $(inputs[2]).find('input').attr('id', 'id_form-' + (i - 1) +'-educ_start');
    $(inputs[2]).find('input').attr('name', 'form-' + (i - 1) +'-educ_start');
    $(inputs[3]).find('label').attr('for', 'id_form-' + (i - 1) +'-educ_end');
    $(inputs[3]).find('input').attr('id', 'id_form-' + (i - 1) +'-educ_end');
    $(inputs[3]).find('input').attr('name', 'form-' + (i - 1) +'-educ_end');
    $(inputs[4]).find('label').attr('for', 'id_form-' + (i - 1) +'-programme');
    $(inputs[4]).find('input').attr('id', 'id_form-' + (i - 1) +'-programme');
    $(inputs[4]).find('input').attr('name', 'form-' + (i - 1) +'-programme');

    i++;
  }
}

function recountEducItemsNums() {
  let items = $('.signup-educ-item');
  let counter = 1;

  for (let item of items) {
    $(item).find('.signup-educ-item-num span').html('#' + counter)

    counter++;
  }
}



$(document).ready(() => {

  let educItemsCount = $('.signup-educ-item').length;

  // Click on the "Sign in" button
  $('#signin-btn').click(e => {
    $('#popup-wrapper').css({
      'visibility': 'visible',
      'opacity': 1
    });

    $('#popup-window').css({
      'transform': 'translateY(0)'
    });
  });


  // Click on the close button in the popup window
  $('#popup-close').click(e => {
    $('#popup-wrapper').css({
      'visibility': 'hidden',
      'opacity': 0
    });

    $('#popup-window').css({
      'transform': 'translateY(40px)'
    });

    setTimeout(() => {
      $('#popup-window').css({
        'transform': 'translateY(-40px)'
      });
    }, 400);
  });

  // Sign up form
  // Add new educations
  $('#signup-addeduc').click(() => {
    educItemsCount++;
    //console.log(educItemsCount)
    let itemsCount = $('.signup-educ-item').length;
    $('input[name="form-TOTAL_FORMS"]').val(itemsCount + 1);

    if (itemsCount < 2) {
      $('#signup-educ').children().first().find('.signup-educ-item-info').removeClass('signup-educ-item-info-hidden');
    }

    let html = `
                <div class="signup-educ-item signup-educ-item-hidden">
                  <div class="signup-educ-item-info">
                    <div class="signup-educ-item-num"><span>#${itemsCount+1}</span></div>
                    <div class="signup-educ-item-del">
                      <span>
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                        	 width="408.483px" height="408.483px" viewBox="0 0 408.483 408.483" style="enable-background:new 0 0 408.483 408.483;"
                        	 xml:space="preserve">
                        	<g>
                        		<path d="M87.748,388.784c0.461,11.01,9.521,19.699,20.539,19.699h191.911c11.018,0,20.078-8.689,20.539-19.699l13.705-289.316
                        			H74.043L87.748,388.784z M247.655,171.329c0-4.61,3.738-8.349,8.35-8.349h13.355c4.609,0,8.35,3.738,8.35,8.349v165.293
                        			c0,4.611-3.738,8.349-8.35,8.349h-13.355c-4.61,0-8.35-3.736-8.35-8.349V171.329z M189.216,171.329
                        			c0-4.61,3.738-8.349,8.349-8.349h13.355c4.609,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.737,8.349-8.349,8.349h-13.355
                        			c-4.61,0-8.349-3.736-8.349-8.349V171.329L189.216,171.329z M130.775,171.329c0-4.61,3.738-8.349,8.349-8.349h13.356
                        			c4.61,0,8.349,3.738,8.349,8.349v165.293c0,4.611-3.738,8.349-8.349,8.349h-13.356c-4.61,0-8.349-3.736-8.349-8.349V171.329z"/>
                        		<path d="M343.567,21.043h-88.535V4.305c0-2.377-1.927-4.305-4.305-4.305h-92.971c-2.377,0-4.304,1.928-4.304,4.305v16.737H64.916
                        			c-7.125,0-12.9,5.776-12.9,12.901V74.47h304.451V33.944C356.467,26.819,350.692,21.043,343.567,21.043z"/>
                        	</g>
                        </svg>
                      </span>
                    </div>
                  </div>

                  <div class="inputline-wrapper">
                    <div class="inputline clearfix university">
                      <div class="inputline-labelblock">
                        <label for="id_form-${itemsCount}-university">Университет</label>
                      </div>
                      <div class="inputline-inputblock">
                        <input type="text" name="form-${itemsCount}-university" maxlength="80" id="id_form-${itemsCount}-university">
                      </div>
                    </div>


                  </div>

                  <div class="inputline-wrapper">
                    <div class="inputline clearfix degree">
                      <div class="inputline-labelblock">
                        <label for="id_form-${itemsCount}-degree">Ступень обучения</label>
                      </div>
                      <div class="inputline-inputblock">
                        <select name="form-${itemsCount}-degree" id="id_form-${itemsCount}-degree">
                          <option value="" selected="">---------</option>
                          <option value="bac">Бакалавриат</option>
                          <option value="mag">Магистратура</option>
                        </select>
                      </div>
                    </div>


                  </div>

                  <div class="inputline-wrapper">
                    <div class="inputline clearfix educ_start">
                      <div class="inputline-labelblock">
                        <label for="id_form-${itemsCount}-educ_start">Год начала</label>
                      </div>
                      <div class="inputline-inputblock">
                        <input type="number" name="form-${itemsCount}-educ_start" id="id_form-${itemsCount}-educ_start">
                      </div>
                    </div>


                  </div>

                  <div class="inputline-wrapper">
                    <div class="inputline clearfix educ_end">
                      <div class="inputline-labelblock">
                        <label for="id_form-${itemsCount}-educ_end">Год окончания</label>
                      </div>
                      <div class="inputline-inputblock">
                        <input type="number" name="form-${itemsCount}-educ_end" id="id_form-${itemsCount}-educ_end">
                      </div>
                    </div>


                  </div>

                  <div class="inputline-wrapper">
                    <div class="inputline clearfix programme">
                      <div class="inputline-labelblock">
                        <label for="id_form-${itemsCount}-programme">Направление обучения</label>
                      </div>
                      <div class="inputline-inputblock">
                        <input type="text" name="form-${itemsCount}-programme" maxlength="100" id="id_form-${itemsCount}-programme">
                      </div>
                    </div>
                  </div>
                </div>
    `;

    $('#signup-educ').append(html);
    //console.log($('#signup-educ').children().last());
    setTimeout(() => {
      $('#signup-educ').children().last().css({
        'visibility': 'visible',
        'opacity': '1',
        'transform': 'translateX(0)'
      });
    }, 10);

  });

  // When clicked on a remove educ item button
  $(document).on('click', '.signup-educ-item-del', e => {
    let itemsCount = $('#signup-educ').children().length;
    $('input[name="form-TOTAL_FORMS"]').val(itemsCount - 1);

    let numClicked = parseInt($(e.target).closest('.signup-educ-item-info').find('.signup-educ-item-num span').html().match(/\d+/)[0]);

    educItemsCount--;

    if ($(e.target).closest('.signup-educ-item').is($('#signup-educ').children().first())) {
      //console.log(true);
      let nextItem = $('#signup-educ').children()[1];
      $(nextItem).css({
        'border-top': 'none',
        'margin-top': '0',
        'padding-top': '0'
      });
    }
    else {
      //console.log(false);
    }

    //console.log(educItemsCount)
    let current = $(e.target).closest('.signup-educ-item');
    let height = $(current).outerHeight();
    $(current).css({'height': height + 'px'});
    $(current).addClass('signup-educ-item-deleted');

    setTimeout(() => {
      $(current).css({
        'height': '0',
        'margin': '0',
        'padding': '0'
      });

      setTimeout(() => {
        $(current).remove();

        if (educItemsCount == 1) {
          $('#signup-educ').children().first().find('.signup-educ-item-info').addClass('signup-educ-item-info-hidden');
        }
        recountEducItems(numClicked);
      }, 400);

    }, 400);
  });

});
