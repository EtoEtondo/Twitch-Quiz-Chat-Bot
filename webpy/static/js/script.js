$(function() {
  startLiveUpdate();
  resetAnswerSelection();
});

let showChatAnswers = false;
let selectedAnswerId = null;

$(".start").click(function() {
  $(".quiz_start").fadeOut(function() {
      startQuiz();
  });
  showChatAnswers = false;
  resetAnswerSelection();
});

function startQuiz() {
  currentQuestionNo = 0;
  points1 = 0;
  points2 = 0;
  $("#point_text_1").text(points1);
  $("#point_text_2").text(points2);
  showNextQuestion();
  $("#question").fadeIn();
  $("#continue_btn").hide();
  $("#answer_commit_btn").show();
  showChatAnswers = false;
  resetAnswerPercentages();
  resetAnswerSelection();
}

$(".answer").click(function() {
  deselectAllAnswers();
  selectAnswer($(this).attr("id"));
  selectedAnswerId = $(this).attr("id");
});

$("#answer_commit_btn").click(function() {
  if (selectedAnswerId) {
      validateAnswer();
      showChatAnswers = true;
      fetchAnswerData();
  } else {
      alert("Please select an answer!");
  }
});

$(".restart").click(function() {
  $(".quiz_end").fadeOut(function() {
      startQuiz();
  });
  showChatAnswers = false;
  resetAnswerSelection();
});

$("#up_1_btn").click(function() {
  points1++;
  $("#point_text_1").text(points1);
});

$("#up_2_btn").click(function() {
  points2++;
  $("#point_text_2").text(points2);
});

$("#down_1_btn").click(function() {
  points1--;
  $("#point_text_1").text(points1);
});

$("#down_2_btn").click(function() {
  points2--;
  $("#point_text_2").text(points2);
});

function validateAnswer() {
  $("#answer_commit_btn").hide();
  $(".answer").prop("disabled", true);
  var rightAnswer = getRightAnswer();
  var selectedAnswerElement = $("#" + selectedAnswerId);
  var selectedAnswer = selectedAnswerElement.text()[0];

  $(".answer").removeClass("btn-primary btn-danger btn-success btn-default");
  $(".answer").addClass("btn-default");

  if (selectedAnswer == rightAnswer){
      selectedAnswerElement.addClass("btn-success");
  } else {
      selectedAnswerElement.addClass("btn-danger");

      //mark right answer
      $(".answer").each(function() {
          if ($(this).text().startsWith(rightAnswer)) {
              $(this).addClass("btn-success");
          }
      });
  }
  $("#continue_btn").show();
}

$("#continue_btn").click(function() {
  currentQuestionNo++;
  showNextQuestion();
  $("#continue_btn").hide();
  $("#answer_commit_btn").show();
  $(".answer").prop("disabled", false);
  showChatAnswers = false;
  resetAnswerPercentages();
  resetAnswerSelection();
});

function updateAnswerPercentages(data) {
  if (showChatAnswers && currentQuestion) {
      $("#answer_a").text(currentQuestion.answers.A + "   " + (data.percentages.A || 0) + "%");
      $("#answer_b").text(currentQuestion.answers.B + "   " + (data.percentages.B || 0) + "%");
      $("#answer_c").text(currentQuestion.answers.C + "   " + (data.percentages.C || 0) + "%");
      $("#answer_d").text(currentQuestion.answers.D + "   " + (data.percentages.D || 0) + "%");
  }
}

function resetAnswerPercentages() {
  if (currentQuestion) {
      $("#answer_a").text(currentQuestion.answers.A);
      $("#answer_b").text(currentQuestion.answers.B);
      $("#answer_c").text(currentQuestion.answers.C);
      $("#answer_d").text(currentQuestion.answers.D);
  }
}

function fetchAnswerData() {
  $.ajax({
      url: "/api/answers",
      method: "GET",
      dataType: "json",
      success: function(data) {
          if (currentQuestion) {
              updateAnswerPercentages(data);
          }
      },
      error: function(error) {
          console.error("Error while getting answers:", error);
      }
  });
}

function startLiveUpdate() {
  setInterval(fetchAnswerData, 1000);
}

function selectAnswer(id) {
  $("#" + id).addClass("btn-primary");
  $("#" + id).removeClass("btn-default");
}

function deselectAllAnswers() {
  $(".answer").removeClass("btn-primary");
  $(".answer").addClass("btn-default");
  selectedAnswerId = null;
}

function resetAnswerSelection() {
  deselectAllAnswers();
  selectedAnswerId = null;
}

function showEnd() {
  $("#question").fadeOut(function() {
      $(".quiz_end").fadeIn();
  });
}