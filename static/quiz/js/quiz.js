function getTimeRemaining(endtime) {
  var t = Date.parse(endtime) - Date.parse(new Date());
  var seconds = Math.floor((t / 1000) % 60);
  var minutes = Math.floor((t / 1000 / 60) % 60);
  var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
  var days = Math.floor(t / (1000 * 60 * 60 * 24));
  return {
    'total': t,
    'days': days,
    'hours': hours,
    'minutes': minutes,
    'seconds': seconds
  };
}

function initializeClock(id, endtime) {
  var clock = document.getElementById(id);
  var daysSpan = clock.querySelector('.days');
  var hoursSpan = clock.querySelector('.hours');
  var minutesSpan = clock.querySelector('.minutes');
  var secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    var t = getTimeRemaining(endtime);

    //daysSpan.innerHTML = t.days;
    hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.total <= 0) {
      clearInterval(timeinterval);
      document.getElementById("clockdiv").style.color = 'red';
      document.getElementById("clockdiv").innerHTML = 'Час вичерпано';
    }
    if (t.total ==  60 * 1000){
      document.getElementById("seconds").style.color = 'red';
    }
    if (document.getElementById("current_question_number_in_quiz").innerHTML != '1'){
    document.getElementById("python3_warning").style.display = 'none';
     }
  }

  updateClock();
  var timeinterval = setInterval(updateClock, 1000);
}

if (top.location.pathname == "/quiz_process" && document.getElementById("current_question_number_in_quiz").innerHTML == '1'){
var number_questions = document.getElementById("number_questions");
var deadline = new Date(Date.parse(new Date()) + number_questions.innerHTML * document.getElementById("time_per_question").value * 1000);
localStorage.setItem("deadline", deadline);
initializeClock('clockdiv', deadline);
}
else if (top.location.pathname == "/quiz_process" && document.getElementById("current_question_number_in_quiz").innerHTML != '1'){
var deadline = localStorage.getItem("deadline");
initializeClock('clockdiv', deadline);
}
