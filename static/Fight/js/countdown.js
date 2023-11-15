document.addEventListener("DOMContentLoaded", function () {
  var countdownElement = document.getElementById("countdown");
  var remainingTime = parseInt(countdownElement.dataset.remainingTime);
  var countdownInterval;

  function startCountdown() {
    countdownInterval = setInterval(updateCountdown, 1000);
    document.getElementById("start-countdown").disabled = true;

    // Setting a unique session key for starting the battle
    var userId = document.getElementById("user-id").value;
    var battleStartTimeKey = "battle_start_time_" + userId;
    var startTime = Math.floor(Date.now() / 1000);
    sessionStorage.setItem(battleStartTimeKey, startTime);
    sessionStorage.setItem("battle_remaining_time", remainingTime);
  }

  function updateCountdown() {
    var minutes = Math.floor(remainingTime / 60);
    var seconds = remainingTime % 60;

    var formattedMinutes = minutes < 10 ? "0" + minutes : minutes;
    var formattedSeconds = seconds < 10 ? "0" + seconds : seconds;

    countdownElement.textContent = formattedMinutes + " minutes " + formattedSeconds + " seconds";

    remainingTime -= 1;

    if (remainingTime <= 0) {
      clearInterval(countdownInterval);

      // Downloading a unique session key to start the battle
      var userId = document.getElementById("user-id").value;
      var battleStartTimeKey = "battle_start_time_" + userId;

      sessionStorage.removeItem(battleStartTimeKey);
      sessionStorage.removeItem("battle_remaining_time");

      window.location.href = countdownElement.dataset.redirectUrl;
    }
  }

  // Checking whether the battle has been started earlier
  var userId = document.getElementById("user-id").value;
  var battleStartTimeKey = "battle_start_time_" + userId;
  var storedStartTime = sessionStorage.getItem(battleStartTimeKey);
  var storedRemainingTime = sessionStorage.getItem("battle_remaining_time");
  if (storedStartTime && storedRemainingTime) {
    var currentTime = Math.floor(Date.now() / 1000);
    var elapsedSeconds = currentTime - parseInt(storedStartTime);
    remainingTime = parseInt(storedRemainingTime) - elapsedSeconds;

    if (remainingTime > 0) {
      startCountdown();
    } else {
      window.location.href = countdownElement.dataset.redirectUrl;
    }
  }

  document.getElementById("start-countdown").addEventListener("click", startCountdown);
});
