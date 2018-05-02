$(document).ready(() => {
  $('#signup-page').removeClass('signup-page-hidden');

  // Check if there is more than one education item
  // and, if true, add additional information on the left
  let educItemsCount = $('.signup-educ').length;
  //console.log(educItemsCount);

  let educItemsAmount = $('.signup-educ-item').length;

  if (educItemsAmount > 1) {
    $('.signup-educ-item').find('.signup-educ-item-info').removeClass('signup-educ-item-info-hidden');
  }

  recountEducItemsNums()
});
