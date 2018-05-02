// Recount education items amount
function recountEducInfoItems(numClicked) {
  $('.educ-info-item').length;

  let items = $('.educ-info-item');

  let i = 1;

  for (let item of items) {
    if (i < numClicked) {
      i++;
      continue;
    }

    let info = $(item).find('.education-num');

    $(info).find('span').css({
      'transform': 'translateX(30px)',
      'opacity': '0',
      'visibility': 'hidden'
    });

    let m = i;
    setTimeout(() => {

      $(info).prepend('<span class="education-num-hidden" style="transform: translateX(-30px);">#' + m + '</span>');
      $(info).find('span')[1].remove();

      setTimeout(() => {
        $(info).find('span').css({
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
    let inputs = $(item).children('.info-line');
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

function recountEducItemsInfoNums() {
  let items = $('.educ-info-item');
  let counter = 1;

  for (let item of items) {
    $(item).find('.education-num span').html('#' + counter)

    counter++;
  }
}

$(document).ready(() => {
  let educItemsCount = $('.educ-info-item').length;
  console.log(educItemsCount)

  $('.myprofile-nav ul li span').click(e => {
    let clicked = e.target;
    let clickedLi = $(clicked).closest('li');
    let currentActive = $('.myprofile-nav ul li span.active');
    let currentActiveLi = $('.myprofile-nav ul li span.active').closest('li');
    let newHeader = $(clicked).html();
    let currentActiveNum;
    let newActiveNum;
    let i = 0;

    let listItems = $('.myprofile-nav ul li');

    for (li of listItems) {

      if (clickedLi.is(li)) {
        newActiveNum = i;
      }

      if (currentActiveLi.is(li)) {
        currentActiveNum = i;
      }

      i++;
    }

    $(currentActive).removeClass('active');
    $(clicked).addClass('active');

    $('.myprofile-body-content > div:nth-child(' + (currentActiveNum + 1) + ')').addClass('myprofile-div-hidden');
    $('.myprofile-body-content > div:nth-child(' + (newActiveNum + 1) + ')').removeClass('myprofile-div-hidden');
    $('#myprofile-body-top-title').html(newHeader);
  });


  // Myprofile edit page scripts
  $('#educ-info-addeduc').click(e => {
    let lastEducItem = $('.educ-info-item').last();
    let id = parseInt($(lastEducItem).find('input[type="hidden"]').attr('value'));

    let itemsCount = $('.educ-info-item').length;
    $('input[name="form-TOTAL_FORMS"]').val(itemsCount + 1);

    if (educItemsCount == 1) {
      $('.educ-info-item').find('.education-num span').removeClass('education-num-hidden');
      $('.educ-info-item').find('.education-num button').removeClass('delete-disabled');
      $('.educ-info-item').find('.education-num button').removeAttr('disabled');
    }

    educItemsCount++;

    let html = `
                <div class="educ-info-item educ-info-item-beforestart">
                  <div class="education-num">
                    <span>#${educItemsCount}</span>
                    <button class="delete" type="button">
                      Удалить
                    </button>
                  </div>

                  <div class="info-line clearfix">
                    <div class="info-line-label">
                      <span>Университет</span>
                    </div>

                    <div class="info-line-body">
                      <input type="text" name="form-${educItemsCount-1}-university" value="" maxlength="80" id="id_form-${educItemsCount-1}-university">
                    </div>
                  </div>

                  <div class="info-line clearfix">
                    <div class="info-line-label">
                      <span>Ступень обучения</span>
                    </div>

                    <div class="info-line-body">
                      <select name="form-${educItemsCount-1}-degree" id="id_form-${educItemsCount-1}-degree">
                        <option value="">---------</option>
                        <option value="bac" selected="">Бакалавриат</option>
                        <option value="mag">Магистратура</option>
                      </select>
                    </div>
                  </div>

                  <div class="info-line clearfix">
                    <div class="info-line-label">
                      <span>Год начала</span>
                    </div>

                    <div class="info-line-body">
                      <input type="number" name="form-${educItemsCount-1}-educ_start" value="" min="1900" max="2025" id="id_form-${educItemsCount-1}-educ_start">
                    </div>
                  </div>

                  <div class="info-line clearfix">
                    <div class="info-line-label">
                      <span>Год окончания</span>
                    </div>

                    <div class="info-line-body">
                      <input type="number" name="form-${educItemsCount-1}-educ_end" value="" min="1900" max="2025" id="id_form-${educItemsCount-1}-educ_end">
                    </div>
                  </div>

                  <div class="info-line clearfix">
                    <div class="info-line-label">
                      <span>Направление обучения</span>
                    </div>

                    <div class="info-line-body">
                      <input type="text" name="form-${educItemsCount-1}-programme" value="" maxlength="100" id="id_form-${educItemsCount-1}-programme">
                    </div>
                  </div>

                  <input type="hidden" name="form-${educItemsCount-1}-id" value="${id+1}" id="id_form-${educItemsCount-1}-id">
                </div>
    `;

    $('#educ-info').append(html);

    // Show and slide new added item
    setTimeout(() => {
      $('#educ-info').children().last().removeClass('educ-info-item-beforestart');
    }, 10);

  });

  $(document).on('click', '.education-num .delete', e => {
    console.log('being deleted')
    let educItem = $(e.target).closest('.educ-info-item');
    let educItemHeight = $(educItem).outerHeight();
    let numClicked = parseInt($(e.target).closest('.education-num').find('span').html().match(/\d+/)[0]);
    educItemsCount--;

    let itemsCount = $('.educ-info-item').length;
    $('input[name="form-TOTAL_FORMS"]').val(itemsCount - 1);

    $(educItem).css({
      'height': educItemHeight + 'px',
      'transform': 'translateX(30px)',
      'opacity': '0'
    });

    setTimeout(() => {
      $(educItem).css({
        'height': '0',
        'margin': '0',
        'padding': '0'
      });

      setTimeout(() => {
        $(educItem).remove();

        if (educItemsCount == 1) {
          $('.educ-info-item').first().find('.education-num span').addClass('education-num-hidden');
          $('.educ-info-item').first().find('.education-num .delete').prop('disabled', true);
          $('.educ-info-item').first().find('.education-num .delete').addClass('delete-disabled');
        }

        recountEducInfoItems(numClicked);
      }, 400);
    }, 400);
  });
});
