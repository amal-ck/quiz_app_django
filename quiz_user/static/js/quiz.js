const showData = document.querySelectorAll('.show-data');
const startQuizBtn = document.getElementById('startQuizBtn')
const closePopupBtn = document.getElementById('closePopupBtn');
const overlay = document.getElementById('overlay');
const quizPopup = document.getElementById('quizPopup');
const popupQuizName = document.getElementById('popupQuizName');
const popupQuizDetails = document.getElementById('popupQuizDetails');

showData.forEach(button => {
    button.addEventListener('click', () => {
        const quizId = button.getAttribute('data-quiz-id');
        const quizName = button.getAttribute('data-quiz-name');
        const quizTime = button.getAttribute('data-quiz-time');
        const quizQn = button.getAttribute('data-quiz-total-qn');
        

        popupQuizName.textContent = quizName;
        popupQuizDetails.textContent = `The ${quizName} quiz consists of ${quizQn} questions. You will have ${quizTime} seconds to complete all questions. All the best!`;
        startQuizBtn.href = `/quiz/${quizId}`;
        
        overlay.style.display = 'block';
        quizPopup.style.display = 'block';
    });
});

closePopupBtn.addEventListener('click', () => {
    overlay.style.display = 'none';
    quizPopup.style.display = 'none';
});

