var tempsRestant = 10;
var ecriture = false;

$(document).ready(function() {
    var inputText = $('#inputText');
    var tempsRestantElement = $("#timer");
    var textBar = $("#textBar");

    var audio = $("#Audio");
    var audioSection = $("#audioSection");

    var spectrogrammeSection = $("#spectrogramSection");

    var prediction = $("#Prediction");
    var predictionElement = $("#predictionSection");

    var statistics = $("#Statistics");
    
    var isRecording = false;
    var audioChunks = [];

    var mode_utilisateur = true;


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

    $(".1").on("click", function() {
        $('html, body').animate({
            scrollTop: audio.offset().top
        }, 1000);
    });

    $(".2").on("click", function() {
        $('html, body').animate({
            scrollTop: prediction.offset().top
        }, 1000);
    });

    $(".3").on("click", function() {
        $('html, body').animate({
            scrollTop: statistics.offset().top
        }, 1000);
    });

    $(".4").on("click", function() {
        $('html, body').animate({
            scrollTop: $('header').offset().top
        }, 1000);
    });


    $('#utilisateur').addClass('bouton-actif');

    $('#utilisateur, #touche').click(function() {
        $('#utilisateur, #touche').removeClass('bouton-actif');
        $(this).addClass('bouton-actif');
        if ($(this).attr('id') == "utilisateur"){
            mode_utilisateur = true;
        }
        else {
            mode_utilisateur = false;
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

                    audioSection.append("<h2 class='audio'>Record</h2>");
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
                spectrogrammeSection.append("<h2 class='spectrogramme'>Spectrogram</h2>");
                spectrogrammeSection.append("<img src='.\\spectrogrammes\\spectrogram.png' class='spectrogramme'></img>");
                predict();
            },
            error: function(xhr, status, error) {
                console.error("Erreur lors de l'envoi de l'audio:", error);
            }
        });
    }

    function predict(){
        var url_mode = "http://127.0.0.1:5000/";
        if (mode_utilisateur){
            url_mode += "predict";
        }
        else {
            url_mode += "predict_letter";
        }

        $.ajax({
            url: url_mode,
            type: "POST",
            success: function() {
                lire_txt();
            },
            error: function() {
                console.error("Erreur");
            }
        });
    }

    function lire_txt(){
        $.ajax({
            url: "lire_txt.php",
            type: "POST",
            dataType: "json",
            data : {mode : mode_utilisateur},
            success: function(response){
                displayPrediction(response.line);
            },
            error: function(){
                console.log('Erreur');
            }
        });
        console.log("Lecture terminée");
    }
    

    function displayPrediction($prediction){
        if (mode_utilisateur){
            predictionElement.html("<p>" + $prediction + "</p>");
        }
        else {
            var comparisonResult = compareStrings(inputText.text(), $prediction);
            var output = "<p>Chaîne initiale: " + inputText.text() + "</p>" + "<p>Prédiction: " + comparisonResult.result + "</p>";
            output += "<p>Nombre de lettres identiques: " + comparisonResult.identicalCount + "</p>";
            output += "<p>Nombre total de lettres: " + comparisonResult.totalCount + "</p>";
            output += "<p>Rapport de correspondance: " + comparisonResult.percentMatch.toFixed(2) + "%</p>";

            predictionElement.html(output);
        }
    }


    function compareStrings(str1, str2) {
        var result = '';
        var maxLength = Math.max(str1.length, str2.length);
        var identicalCount = 0;
    
        for (var i = 0; i < maxLength; i++) {
            var char1 = i < str1.length ? str1.charAt(i) : '';
            var char2 = i < str2.length ? str2.charAt(i) : '';
    
            if (char1 === char2) {
                result += '<span class="same">' + char2 + '</span>';
                identicalCount++;
            } else {
                result += '<span class="different">' + char2 + '</span>';
            }
        }
    
        var totalCount = Math.max(str1.length, str2.length);
        var percentMatch = (identicalCount / totalCount) * 100;
    
        return {result: result, identicalCount: identicalCount, totalCount: totalCount, percentMatch: percentMatch};
    }    
});


