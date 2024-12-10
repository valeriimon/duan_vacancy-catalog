$(document).ready(function () {

  $('.save-resume-btn').click(function (ev) {
    ev.preventDefault();
    const el = $(this);
    const resumeId = el.data('id')
    if (!resumeId) {
      return;
    }
    saveItemToUser({
      url: '/resume/save-resume-to-user/',
      data: { resume_id: resumeId },
      el,
    });
  });

  $('.save-vacancy-btn').click(function (ev) {
    ev.preventDefault();
    const el = $(this);
    const vacancyId = el.data('id')
    if (!vacancyId) {
      return;
    }
    saveItemToUser({
      url: '/vacancy/save-vacancy-to-user/',
      data: { vacancy_id: vacancyId },
      el,
    });
  });

  function saveItemToUser(config) {
    $.ajax({
      url: config.url,
      type: "POST",
      data: config.data,
      beforeSend: function (xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", $(document.body).data('csrftoken'));
    },
      success: function (response) {
          config.el.addClass('saved')
          config.el.html(`
            <i class="bi bi-check2"></i>
             Збережено
            `)
          config.el.prop('disabled', true)
      },
      error: function (response) {
          alert("Error saving!");
      }
    });
  }
  
});