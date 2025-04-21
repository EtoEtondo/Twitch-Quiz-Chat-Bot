var currentQuestionNo = 0;
var points1 = 0;
var points2 = 0;
var currentQuestion;

var questions = [
  {
    "id":"1",
    "question" : "Example: Is Timo cool?",
    "answers" : {
      "A":"Yes",
      "B":"Maybe",
      "C":"No",
      "D":"Who is Timo?"
    }, 
    "right":"D"
  },{
    "id":"2",
    "question" : "What Pokedex number does Arceus have in the Hisui-Dex?",
    "answers" : {
      "A":"231",
      "B":"229",
      "C":"238",
      "D":"242"
    }, 
    "right":"C"
  },{
    "id":"3",
    "question" : "Which Pokémon attack the Professor at the beginning of the game in Generation 3?",
    "answers" : {
      "A":"Poochyena",
      "B":"Pidgey",
      "C":"Zigzagoon",
      "D":"Seedot"
    }, 
    "right":"A"
  }
];

function showNextQuestion() {
  if (currentQuestionNo >= questions.length) {
    showEnd();
    currentQuestionNo = 0;
  }
  console.log("Loading Question:" + currentQuestionNo);
  currentQuestion = questions[currentQuestionNo];
  $("#qno").text(currentQuestionNo);
  $("#question_text").text(currentQuestion.question);
  $("#answer_a").text(currentQuestion.answers.A);
  $("#answer_b").text(currentQuestion.answers.B);
  $("#answer_c").text(currentQuestion.answers.C);
  $("#answer_d").text(currentQuestion.answers.D); 
  
  $(".answer").removeClass("btn-primary btn-danger btn-success btn-default");
  $(".answer").addClass("btn-default");
}

function getRightAnswer() {
  return currentQuestion.right;
}