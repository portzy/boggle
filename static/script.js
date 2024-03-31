$(document).ready(function(){
        let score = 0;

        let timeLeft = 60;
        const timerElement = $('#timer');
        const guessForm = $('#guess-form');
    
        let timerId = setInterval(function() {
            if (timeLeft > 0) {
                timeLeft -= 1;
                timerElement.text(timeLeft);
            } else {
                clearInterval(timerId);
                guessForm.find('input, button').attr('disabled', true);
                $('#result').text('Time is up!');
                
                // send game statistics
                axios.post('/end-game', { score: score })
                    .then(function(response) {
                        $('#times-played').text('games played: ' + response.data.times_played);
                        $('#highest score').text('highest score ' + response.data.highest_score);
                    })
                    .catch(function(error) {
                        console.error('Error sending game statistics:', error);
                    });
            }
        }, 1000);
        

    $('#guess-form').on('submit', function(event){
        event.preventDefault(); //prevents from refreshing
        let userGuess = $('#guess').val().toLowerCase(); //gets value from guess form

        axios.post('/check-word', { guess: userGuess}) //sends POST request to server
            .then(function(response){
                const resultElement = $('#result');

                if(response.data.result === 'ok'){
                    resultElement.text('the word is valid!');
                    score += userGuess.length;
                    $('#score').text(score); //updates score display
                } else if(response.data.result === 'not-on-board'){
                    resultElement.text('the word is not on the board.');
                } else if(response.data.result === 'not-word') {
                    resultElement.text('that is not a valid word.');
                }

            })
            .catch(function(error){
                console.error(error);
                $('#result').text('an error occured');
            })

    })

})