var tempsRestant = 10;
var ecriture = false;

$(document).ready(function() {
    var inputText = $('#inputText');
    var tempsRestantElement = $("#timer");
    var textBar = $("#textBar");
    var audioSection = $("#audioSection");
    var spectrogrammeSection = $("#spectrogramSection");
    
    var isRecording = false;
    var audioChunks = [];

    $("#textBar").on("input", function() {
        if (!ecriture){
            ecriture = true;
        
            var intervalId = setInterval(function() {
                if (ecriture){
                    tempsRestant--;

                    var secondes = tempsRestant % 60;
                    var temps = "0:";
                    if (secondes < 10){
                        temps += "0";
                    }
                    temps += secondes;
                    tempsRestantElement.text(temps);
        
                    if (tempsRestant == 0) {
                        clearInterval(intervalId);
                        textBar.prop("disabled", true);
                    }
                }
                else {
                    clearInterval(intervalId);
                }
            }, 1000);
        }
        inputText.text(textBar.val());

        if (!isRecording) {
            isRecording = true;
            startRecording();
        }
    });

    $("#resetButton").on("click", function() {
        if (tempsRestant < 60) {            
            ecriture = false;
            textBar.prop("disabled", false);
            textBar.val("");
            inputText.text("");

            tempsRestant = 10;
            tempsRestantElement.text("0:10");
            isRecording = false;
            $(".audio").remove();
            $(".spectrogramme").remove();
        }
    }); 

    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function(stream) {
                var mediaRecorder = new MediaRecorder(stream);
    
                mediaRecorder.ondataavailable = function(e) {
                    if (e.data.size > 0) {
                        audioChunks.push(e.data);
                    }
                };
    
                mediaRecorder.onstop = function() {
                    var audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    var audioUrl = URL.createObjectURL(audioBlob);

                    audioSection.append("<h2 class='audio'>Enregistrement</h2>");
                    audioSection.append("<audio controls src='" + audioUrl + "' class='audio'></audio>");

                    sendDataToBackend(audioBlob);
                    audioChunks = [];
                };
    
                mediaRecorder.start();
    
                setTimeout(function() {
                    stopRecording(mediaRecorder);
                }, 10000);
            })
            .catch(function(err) {
                console.error("Erreur lors de l'accès au microphone:", err);
            });
    }
    
    function stopRecording(mediaRecorder) {
        if (isRecording) {
            mediaRecorder.stop();
        }
    }

    function sendDataToBackend(audioBlob) {
        var formData = new FormData();
        formData.append("audio", audioBlob);
    
        $.ajax({
            url: "http://127.0.0.1:5000/upload", 
            type: "POST",
            data: formData,
            processData: false, 
            contentType: false, 
            success: function(data) {
                console.log("Réponse du serveur:", data);
                spectrogrammeSection.append("<h2 class='spectrogramme'>Spectrogramme</h2>");
                spectrogrammeSection.append("<img src='.\\spectrogrammes\\spectrogram.png' class='spectrogramme'></img>");
            },
            error: function(xhr, status, error) {
                console.error("Erreur lors de l'envoi de l'audio:", error);
            }
        });
    }
    
});