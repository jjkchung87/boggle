


class Boggle {
    constructor(remainingTime=15){
        this.runningScore = 0;
        this.remainingTime=remainingTime;
        this.intervalId;
        this.submittedWords = []
        
        this.decreaseRemainingTime()
    }

    async handleSubmit(word){
        if(!this.submittedWords.includes(word)){
            let res = await axios.get('http://127.0.0.1:5000/check-word',{params:{word: word}})
            console.log(res)
            this.increaseGameScore(res,word)
        }
    }

    increaseGameScore(res,word){
        if(res.data.result === 'ok'){
        this.runningScore += word.length
        this.submittedWords.push(word)
        $('#game-score').html(`<b>Game Score:</b> ${this.runningScore}`)
        }
    }

    decreaseRemainingTime(){
        this.intervalId = setInterval(() => {
            this.remainingTime -= 1;
            $('#countdown-clock').html(`<b>Time Left:</b> ${this.remainingTime}`)

            if (this.remainingTime === 0){
                this.endGame()
            }
        },1000)
    }

    async endGame (){
        clearInterval(this.intervalId);
        alert('Game Over!')
        $('#word-form').on('submit',() => {
            alert('refresh page to play again!')
        })

        this.sendScore()
    }



    async sendScore(){
        let res = await axios.post('http://127.0.0.1:5000/game-end', {score: this.runningScore})

    }

}


const boggle = new Boggle()

async function submitWord(evt){
    evt.preventDefault();
    let word = $('#word-input').val();
    await boggle.handleSubmit(word)
    $('#word-input').val('');
}

$('#word-form').on('submit',submitWord)

//Handles word submissions


//Intializes gamescore in local Storage
// localStorage.setItem('score',0)

//Increases game score when user submits a valid word


//Countdown clock 

//Clock runs out and game ends




    // async handleHighScore() {
    //     if (!localStorage.getItem('highScore')){
    //         localStorage.setItem('highScore',this.runningScore)
    //     } else {
    //         if(parseInt(localStorage.getItem('highScore')) < this.runningScore) {
    //             localStorage.setItem('highScore',this.runningScore)
    //         }    
    //     }
    //     let highScore = parseInt(localStorage.getItem('highScore'))

    //     await this.sendHighScore(highScore)
    // }


