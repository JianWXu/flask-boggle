class Boggle {
  constructor(boardId) {
    this.board = $("#" + boardId);
    this.words = new Set();
    $("#form", this.board).on("submit", this.submitForm.bind(this));
    this.score = 0;
    this.timeLeft = 60;
    this.timer;
  }

  async submitForm(e) {
    e.preventDefault();
    const textInput = $("#text-input", this.board);
    let formData = $(textInput).val();

    if (!formData) return;
    if (this.words.has(formData)) {
      this.showMessage(`Already found this ${word}`, "error");
      return;
    }
    const res = await axios.get("/check-word", { params: { word: formData } });

    if (res.data.result === "not-word") {
      $("#word-length").hide();
      return this.showMessage("This is not a word!", "error");
    } else if (res.data.result === "not-on-board") {
      $("#word-length").hide();
      return this.showMessage("This word is not on the game board!", "error");
    } else {
      this.score += formData.length;
      $("#word-length")
        .show()
        .html("You just scored " + formData.length + "!");
      $("#current-score").text(this.score);
      return this.showMessage("Congrats, this is correct", "ok");
    }

    textInput.val("").focus();
  }

  showMessage(message, cls) {
    $("#submit-message", this.board).text(message).removeClass().addClass(cls);
  }

  async gameOver() {
    clearInterval(this.timer);
    $("#game-over").show();
    $("#playAgainButton").show();
    await this.sendScore();
  }

  updateTimer() {
    this.timeLeft -= 1;
    if (this.timeLeft >= 0) {
      $("#timer").text(this.timeLeft);
    } else {
      this.gameOver();
    }
  }

  start() {
    this.timer = setInterval(() => {
      this.updateTimer();
    }, 1000);
    this.updateTimer();
    $("#playAgainButton").hide();
  }

  async sendScore() {
    const res = await axios.post("/high-score", { score: this.score });
    console.log(res);
  }
}
