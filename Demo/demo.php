<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="demo.css">
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script src="demo.js"></script>
    <title>Demo</title>
</head>
<body>
    <header>
        <h1>Keyboard Acoustic Emanations Analysis</h1>
        <h1>Demo Version</h1>
        <p></p>
    </header>

    <button id="utilisateur">Reconnaissance d'utilisateurs</button>
    <button id="touche">Reconnaissance de touches</button>

    <section id = "text">
        <p id="inputText"></p>
    </section>

    <section id = "inputBar">
            <input type="text" id="textBar" placeholder="Saisissez votre texte ici...">
            <div id="tempsRestant"><p id="timer">0:10</p></div>
            <button onclick="reset()" id="resetButton">
                <img src="reset.png" id = "imageReset">
            </button>
    </section>
    <button class="scroll 1">Voir les résultats</button>
    
    <section class="loadingSection">
    </section>

    <section id = "Audio">
        <h1>Audio</h1>
        <section id="audioSection"></section>
        <section id="spectrogramSection"></section>
        <button class="scroll 2">Voir les résultats</button>
    </section>

    <section class="loadingSection">
    </section>

    <section id = "Prediction">
        <h1>Prediction</h1>
        <section id="predictionSection"></section>
        <button class="scroll 3">Voir les résultats</button>
    </section>
</body>
</html>